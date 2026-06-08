import gradio as gr
from agent import graph

def run_essay_writer(task: str, max_revisions: int, model_name: str):
    import os
    os.environ["OLLAMA_MODEL"] = model_name

    import agent as ag
    from langchain_ollama import ChatOllama
    ag.model = ChatOllama(model=model_name, temperature=0)

    thread = {"configurable": {"thread_id": "1"}}
    state = {
        "task": task,
        "max_revisions": int(max_revisions),
        "revision_number": 1,
    }

    plan_out = research_out = draft_out = critique_out = final_out = ""
    steps_log = ""

    for step in graph.stream(state, thread):
        node_name = list(step.keys())[0]
        node_data = step[node_name]

        if node_name == "planner":
            plan_out = node_data.get("plan", "")
            steps_log += f"[Planner] 개요 작성 완료\n"
        elif node_name == "research_plan":
            content = node_data.get("content", [])
            research_out = f"검색 결과 {len(content)}개 수집\n\n" + "\n---\n".join(content[:4])
            steps_log += f"[Research Plan] 자료 {len(content)}개 수집\n"
        elif node_name == "generate":
            draft_out = node_data.get("draft", draft_out)
            rev = node_data.get("revision_number", "?")
            steps_log += f"[Generate] 초안 작성 (revision {rev})\n"
        elif node_name == "reflect":
            critique_out = node_data.get("critique", "")
            steps_log += f"[Reflect] 피드백 생성 완료\n"
        elif node_name == "research_critique":
            content = node_data.get("content", [])
            steps_log += f"[Research Critique] 추가 자료 {len(content)}개 수집\n"

        yield plan_out, research_out, draft_out, critique_out, steps_log

    final_out = draft_out
    yield plan_out, research_out, final_out, critique_out, steps_log


with gr.Blocks(title="Essay Writer (Ollama)", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Essay Writer — LangGraph + Ollama")
    gr.Markdown("LangGraph 기반 에세이 작성 에이전트. 계획 → 조사 → 작성 → 반성 → 반복")

    with gr.Row():
        with gr.Column(scale=1):
            task_input = gr.Textbox(
                label="에세이 주제",
                placeholder="예: What is the difference between LangChain and LangGraph?",
                lines=3,
            )
            model_input = gr.Textbox(
                label="Ollama 모델",
                value="llama3.2",
                placeholder="llama3.2, gemma3, mistral ...",
            )
            max_rev_slider = gr.Slider(
                label="최대 수정 횟수",
                minimum=1,
                maximum=5,
                step=1,
                value=2,
            )
            run_btn = gr.Button("에세이 작성 시작", variant="primary")

        with gr.Column(scale=2):
            steps_output = gr.Textbox(label="진행 상황", lines=8, interactive=False)

    with gr.Tabs():
        with gr.TabItem("개요 (Plan)"):
            plan_output = gr.Textbox(label="에세이 개요", lines=12, interactive=False)
        with gr.TabItem("조사 자료 (Research)"):
            research_output = gr.Textbox(label="수집된 자료", lines=12, interactive=False)
        with gr.TabItem("최종 에세이 (Draft)"):
            draft_output = gr.Textbox(label="작성된 에세이", lines=20, interactive=False)
        with gr.TabItem("피드백 (Critique)"):
            critique_output = gr.Textbox(label="반성 및 피드백", lines=12, interactive=False)

    run_btn.click(
        fn=run_essay_writer,
        inputs=[task_input, max_rev_slider, model_input],
        outputs=[plan_output, research_output, draft_output, critique_output, steps_output],
    )

if __name__ == "__main__":
    demo.launch()
