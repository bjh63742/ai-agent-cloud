```python
@register_tool(
    description="Analyze code quality and suggest improvements",
    tags=["code_quality"]
)
def analyze_code_quality(action_context: ActionContext, code: str) -> str:
    # 메모리에서 대화 이력 가져오기
    memory = action_context.get_memory()
    
    development_context = []
    for mem in memory.get_memories():
        if mem["type"] == "user":
            development_context.append(f"User: {mem['content']}")
        elif mem["type"] == "assistant" and "Here's the implementation" in mem["content"]:
            development_context.append(f"Implementation Decision: {mem['content']}")
    
    review_prompt = f"""개발 이력을 바탕으로 코드를 리뷰하세요:

개발 이력:
{'\n'.join(development_context)}

현재 구현:
{code}

분석 항목:
1. 모든 요구사항을 충족하는가?
2. 논의된 제약과 고려사항이 반영됐는가?
3. 누락된 요구사항이나 제약은 없는가?
4. 논의된 범위 안에서 개선할 수 있는 것은?
"""
    
    generate_response = action_context.get("llm")
    return generate_response(review_prompt)
```

## 인증(Auth) 의존성 처리

```python
@register_tool(
    description="Update code review status in project management system",
    tags=["project_management"]
)
def update_review_status(action_context: ActionContext,
                         review_id: str,
                         status: str) -> dict:
    # 요청별 인증 토큰을 컨텍스트에서 가져옴
    auth_token = action_context.get("auth_token")
    if not auth_token:
        raise ValueError("Authentication token not found in context")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"https://...someapi.../reviews/{review_id}/status",
        headers=headers,
        json={"status": status}
    )
    
    if response.status_code != 200:
        raise ValueError(f"Failed to update review status: {response.text}")
        
    return {"status": "updated", "review_id": review_id}
```


## 에이전트가 ActionContext를 만드는 방법

```python
def run(self, user_input: str, memory=None, action_context_props=None):
    memory = memory or Memory()
    
    # 필요한 모든 자원을 ActionContext에 담아서 전달
    action_context = ActionContext({
        'memory': memory,
        'llm': self.generate_response,
        **action_context_props  # 요청별 추가 정보 (인증 토큰 등)
    })
    
    while True:
        prompt = self.construct_prompt(action_context, self.goals, memory)
        response = self.prompt_llm_for_action(action_context, prompt)
        result = self.handle_agent_response(action_context, response)
        
        if self.should_terminate(action_context, response):
            break

# 사용 예시
some_agent.run(
    "Update the project status...",
    memory=...,
    action_context_props={"auth_token": "my_auth_token"}
)
```