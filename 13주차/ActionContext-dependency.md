## 도구별 필요 의존성 예시

```python
# 단순한 도구 — 아무 의존성도 필요 없음
@register_tool(description="Convert text to uppercase")
def to_uppercase(text: str) -> str:
    return text.upper()


# 외부 서비스를 호출하는 도구 — 인증 토큰 필요
@register_tool(description="Update user profile")
def update_profile(action_context: ActionContext,
                   username: str,
                   _auth_token: str) -> dict:
    return make_authenticated_request(_auth_token, username)
```

---

## 나쁜 접근: 에이전트가 직접 의존성을 관리

```python
def handle_agent_response(self, action_context: ActionContext, response: str) -> dict:
    action_def, action = self.get_action(response)
    
    args = action["args"].copy()
    if needs_action_context(action_def):
        args["action_context"] = action_context
    if needs_auth_token(action_def):
        args["_auth_token"] = action_context.get("auth_token")
    if needs_user_config(action_def):
        args["_user_config"] = action_context.get("user_config")
        
    result = action_def.execute(**args)
    return result
```

에이전트가 **"무슨 행동을 할지"** 결정하는 것에 집중해야 하는데,
의존성 관리까지 떠맡으면 코드가 지저분해지고 유지보수가 어려워진다.

---

## 좋은 접근: 환경(Environment)이 의존성을 처리

```python
def handle_agent_response(self, action_context: ActionContext, response: str) -> dict:
    action_def, action = self.get_action(response)
    result = self.environment.execute_action(self, action_context, action_def, action["args"])
    return result
```

에이전트는 환경에 전부 넘기고, 환경이 알아서 처리한다. 훨씬 깔끔하다.

---

## 환경(Environment)에서 의존성 자동 주입

```python
class PythonEnvironment(Environment):
    def execute_action(self, agent, action_context: ActionContext,
                       action: Action, args: dict) -> dict:
        try:
            args_copy = args.copy()

            # 도구 함수가 action_context 파라미터를 갖고 있으면 주입
            if has_named_parameter(action.function, "action_context"):
                args_copy["action_context"] = action_context

            # _로 시작하는 파라미터에는 action_context에서 매칭되는 값을 주입
            for key, value in action_context.properties.items():
                param_name = "_" + key
                if has_named_parameter(action.function, param_name):
                    args_copy[param_name] = value

            result = action.execute(**args_copy)
            return self.format_result(result)
        except Exception as e:
            return {"tool_executed": False, "error": str(e)}
```