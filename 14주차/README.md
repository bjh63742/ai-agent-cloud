# 14주차: Agentic Search, Essay Writer, ReAct Pattern

LangGraph와 Ollama를 활용한 에이전트 패턴 실습 프로젝트입니다.

## 프로젝트 구성

| 파일 | 설명 |
|------|------|
| `agentic_search.py` | Tavily + DuckDuckGo를 이용한 에이전틱 검색 |
| `agentic_search.ipynb` | 위 내용의 Jupyter Notebook 버전 |
| `langgraph_components.ipynb` | ReAct 패턴 구현 (단일 턴 + 자동 루프) Notebook |
| `search_agent.py` | LangGraph + Tavily 기반 검색 에이전트 |
| `essay_agent.py` | LangGraph 기반 에세이 작성 에이전트 (핵심 로직) |
| `essay_main.py` | 에세이 에이전트 CLI 실행 |
| `essay_app.py` | 에세이 에이전트 Gradio 웹 UI |

## 사전 요구사항

- Python 3.12
- [uv](https://docs.astral.sh/uv/) 패키지 매니저
- [Ollama](https://ollama.com/) (로컬 LLM 실행)
- Tavily API 키 (`agentic_search.py`, `search_agent.py` 사용 시)

## 설치

### 1. 의존성 설치

```bash
uv sync
```

### 2. Ollama 모델 다운로드

```bash
# ReAct 패턴 예제용
ollama pull qwen2.5-coder:7b

# Essay Writer용 (기본값)
ollama pull llama3.2
```

### 3. 환경변수 설정

`.env` 파일에 Tavily API 키를 설정합니다.

```bash
# .env
TAVILY_API_KEY=your_tavily_api_key_here
```

> Tavily API 키는 [https://tavily.com](https://tavily.com) 에서 무료로 발급받을 수 있습니다.

## 실행 방법

### Agentic Search

Tavily와 DuckDuckGo를 이용한 웹 검색 예제입니다.

```bash
uv run python agentic_search.py
```

또는 Jupyter Notebook으로 실행:

```bash
uv run jupyter notebook agentic_search.ipynb
```

### ReAct 패턴 (Notebook)

단일 턴과 자동 루프 방식을 모두 담은 노트북입니다. Ollama(`qwen2.5-coder:7b`)를 사용합니다.

```bash
uv run jupyter notebook langgraph_components.ipynb
```

### Search Agent (LangGraph)

LangGraph + Tavily + Ollama로 만든 멀티턴 검색 에이전트입니다.

```bash
uv run python search_agent.py
```

### Essay Writer — CLI

주제를 입력하면 계획 → 조사 → 작성 → 반성 → 수정 단계를 거쳐 에세이를 작성합니다.

```bash
uv run python essay_main.py
```

실행 후 에세이 주제를 입력하세요:

```
에세이 주제를 입력하세요: What is the difference between LangChain and LangGraph?
```

### Essay Writer — Gradio 웹 UI

브라우저에서 에세이 작성 과정을 실시간으로 확인할 수 있습니다.

```bash
uv run python essay_app.py
```

실행 후 브라우저에서 `http://localhost:7860` 으로 접속합니다.

웹 UI에서는 다음을 설정할 수 있습니다:
- 에세이 주제
- Ollama 모델 이름 (기본값: `llama3.2`)
- 최대 수정 횟수 (1~5회)

## Essay Writer 동작 흐름

```
입력 주제
    │
    ▼
[Planner]  에세이 개요 작성
    │
    ▼
[Research Plan]  DuckDuckGo로 관련 자료 수집
    │
    ▼
[Generate]  초안 작성
    │
    ▼
[Reflect]  피드백 생성
    │
    ▼
[Research Critique]  추가 자료 수집
    │
    ▼
[Generate]  수정본 작성  ←─ max_revisions 초과 시 종료
```
