import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from duckduckgo_search import DDGS

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
model = ChatOllama(model=OLLAMA_MODEL, temperature=0)
memory = MemorySaver()

PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an essay. \
Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes \
or instructions for the sections."""

WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 5-paragraph essays.\
Generate the best essay possible for the user's request and the initial outline. \
If the user provides critique, respond with a revised version of your previous attempts. \
Utilize all the information below as needed:

------

{content}"""

REFLECTION_PROMPT = """You are a teacher grading an essay submission. \
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, depth, style, etc."""

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can \
be used when writing the following essay. Generate a list of search queries that will gather \
any relevant information. Only generate 3 queries max.

Respond ONLY with a JSON object in this exact format:
{{"queries": ["query1", "query2", "query3"]}}"""

RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can \
be used when making any requested revisions (as outlined below). \
Generate a list of search queries that will gather any relevant information. Only generate 3 queries max.

Respond ONLY with a JSON object in this exact format:
{{"queries": ["query1", "query2", "query3"]}}"""


class Queries(BaseModel):
    queries: List[str]


class AgentState(TypedDict):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int


def ddg_search(query: str, max_results: int = 2) -> list[str]:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [r.get("body", "") for r in results if r.get("body")]
    except Exception:
        return []


def plan_node(state: AgentState):
    messages = [
        SystemMessage(content=PLAN_PROMPT),
        HumanMessage(content=state["task"]),
    ]
    response = model.invoke(messages)
    return {"plan": response.content}


def research_plan_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_PLAN_PROMPT),
        HumanMessage(content=state["task"]),
    ])
    content = list(state.get("content") or [])
    for q in queries.queries:
        content.extend(ddg_search(q, max_results=2))
    return {"content": content}


def generation_node(state: AgentState):
    content = "\n\n".join(state.get("content") or [])
    user_message = HumanMessage(
        content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}"
    )
    messages = [
        SystemMessage(content=WRITER_PROMPT.format(content=content)),
        user_message,
    ]
    response = model.invoke(messages)
    return {
        "draft": response.content,
        "revision_number": state.get("revision_number", 1) + 1,
    }


def reflection_node(state: AgentState):
    messages = [
        SystemMessage(content=REFLECTION_PROMPT),
        HumanMessage(content=state["draft"]),
    ]
    response = model.invoke(messages)
    return {"critique": response.content}


def research_critique_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
        HumanMessage(content=state["critique"]),
    ])
    content = list(state.get("content") or [])
    for q in queries.queries:
        content.extend(ddg_search(q, max_results=2))
    return {"content": content}


def should_continue(state: AgentState):
    if state["revision_number"] > state["max_revisions"]:
        return END
    return "reflect"


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", plan_node)
    builder.add_node("research_plan", research_plan_node)
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.add_node("research_critique", research_critique_node)

    builder.set_entry_point("planner")
    builder.add_edge("planner", "research_plan")
    builder.add_edge("research_plan", "generate")
    builder.add_conditional_edges(
        "generate",
        should_continue,
        {END: END, "reflect": "reflect"},
    )
    builder.add_edge("reflect", "research_critique")
    builder.add_edge("research_critique", "generate")

    return builder.compile(checkpointer=memory)


graph = build_graph()
