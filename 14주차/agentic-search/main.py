from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch


tool = TavilySearch(max_results=4)
print(type(tool))
print(tool.name)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_llm(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
    

prompt = """당신은 똑똑한 리서치 어시스턴트입니다. 검색 엔진을 사용하여 정보를 찾아보세요. \
여러 번 검색을 수행할 수 있습니다(동시에 또는 순차적으로). \
무엇을 찾고 싶은지 확실할 때만 검색하세요. \
후속 질문을 하기 전에 정보를 먼저 찾아야 한다면, 그렇게 해도 됩니다!
"""

model = ChatOllama(model="qwen2.5-coder:7b")
abot = Agent(model, [tool], system=prompt)

messages = [HumanMessage(content="샌프란시스코의 날씨는 어때?")]
result = abot.graph.invoke({"messages": messages})

print(result['messages'][-1].content)

messages = [HumanMessage(content="샌프란시스코와 LA의 날씨는 어때?")]
result = abot.graph.invoke({"messages": messages})

print(result['messages'][-1].content)

query = "2024년 슈퍼볼에서 우승한 팀은 어디인가요? 우승팀의 본부는 어느 주에 있나요? \
그 주의 GDP는 얼마인가요? 각 질문에 답해주세요."
messages = [HumanMessage(content=query)]

model = ChatOllama(model="qwen2.5-coder:7b")
abot = Agent(model, [tool], system=prompt)
result = abot.graph.invoke({"messages": messages})

print(result['messages'][-1].content)