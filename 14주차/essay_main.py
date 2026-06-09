from essay_agent import graph


def main():
    thread = {"configurable": {"thread_id": "1"}}
    task = input("에세이 주제를 입력하세요: ").strip()
    if not task:
        task = "What is the difference between LangChain and LangGraph?"

    state = {
        "task": task,
        "max_revisions": 2,
        "revision_number": 1,
    }

    print(f"\n[시작] 주제: {task}\n{'='*60}")
    for step in graph.stream(state, thread):
        node = list(step.keys())[0]
        data = step[node]
        print(f"\n[{node.upper()}]")
        if "plan" in data:
            print(data["plan"])
        if "draft" in data:
            print(data["draft"][:500] + "..." if len(data["draft"]) > 500 else data["draft"])
        if "critique" in data:
            print(data["critique"][:300] + "..." if len(data["critique"]) > 300 else data["critique"])
        if "content" in data:
            print(f"수집된 자료: {len(data['content'])}개")
    print(f"\n{'='*60}\n[완료]")


if __name__ == "__main__":
    main()
