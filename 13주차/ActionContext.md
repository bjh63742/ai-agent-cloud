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