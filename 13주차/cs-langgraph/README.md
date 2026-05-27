# cs-langgraph

LangGraph 기반 CS 상담 멀티에이전트 프로젝트입니다.

---

## LangGraph란?

**LangGraph**는 LangChain 팀이 만든 에이전트 오케스트레이션 프레임워크입니다.  
핵심 아이디어는 **에이전트 흐름을 방향 그래프(DAG / Cyclic Graph)로 명시적으로 정의**하는 것입니다.

### 핵심 개념

| 개념 | 설명 |
|------|------|
| **State** | 그래프 전체에서 공유되는 데이터 구조 (`TypedDict`). 각 노드는 이 상태를 읽고 업데이트한다. |
| **Node** | 상태를 입력받아 일부를 변경해 반환하는 함수. LLM 호출, 도구 실행 등 하나의 작업 단위. |
| **Edge** | 노드 간 연결. 항상 다음 노드로 이동하는 **일반 엣지**와, 상태 값에 따라 분기하는 **조건부 엣지**가 있다. |
| **StateGraph** | 노드와 엣지를 등록해 그래프를 조립하는 빌더 클래스. |
| **compile()** | 그래프를 실행 가능한 `Runnable`로 컴파일한다. 이후 `.invoke()` / `.stream()`으로 실행. |

### 다른 프레임워크와 비교

| | ADK | CrewAI | **LangGraph** |
|---|---|---|---|
| 흐름 정의 방식 | LLM이 자율적으로 서브에이전트 호출 | 순차/병렬 태스크 선언 | **노드 + 엣지로 그래프 명시** |
| 라우팅 제어 | 암묵적 (LLM 판단) | 암묵적 (태스크 순서) | **명시적 (조건부 엣지 함수)** |
| 상태 관리 | 없음 (프롬프트 내 처리) | 없음 (Flow State 별도) | **TypedDict로 타입 안전하게 관리** |
| 복잡한 분기 | 어려움 | 어려움 | **강점** |
| 보일러플레이트 | 적음 | 중간 | 많음 |
| LLM 독립성 | Google Gemini 전용 | 다양한 LLM 지원 | LangChain 통해 어떤 LLM도 가능 |

### 이 프로젝트의 그래프 구조

```
[START]
   │
   ▼
receptionist          ← 고객 문의 접수 & 유형 분류
   │
   ├─ [기술지원필요] ──▶ tech_support ──▶ [END]
   │
   └─ 일반 문의 ──────▶ finalize_general ──▶ [END]
```

- `receptionist`: 고객 메시지를 분석해 기술 문의면 `[기술지원필요]` 접두어를 붙인다.
- `route()`: `reception_result`를 보고 다음 노드를 결정하는 **조건부 엣지 함수**.
- `tech_support`: 기술 문제를 단계별로 해결해 준다.
- `finalize_general`: 일반 문의는 접수 담당자의 답변을 최종 응답으로 확정한다.

---

## 설치

### 사전 요구사항

- Python 3.10 이상
- [uv](https://github.com/astral-sh/uv) 패키지 매니저
- [Ollama](https://ollama.com) 설치 및 모델 준비

### Ollama 모델 준비

```bash
ollama pull qwen2.5-coder:7b
```

### 프로젝트 설치

```bash
cd cs-langgraph
uv sync
```

---

## 실행

### 채팅 실행

```bash
uv run chat
```

각 노드 실행 시 입력값과 출력값이 함께 출력됩니다.

```
고객: 컴퓨터가 고장났어

  ┌─ [접수 담당자]
  │  입력 user_message: 컴퓨터가 고장났어
  │  출력 reception_result: [기술지원필요] 하드웨어 고장 문의
  └─ 완료

  ┌─ [기술 지원]
  │  입력 user_message: 컴퓨터가 고장났어
  │  출력 response: 안녕하세요! 컴퓨터 문제를 도와드리겠습니다...
  └─ 완료

상담원: 안녕하세요! 컴퓨터 문제를 도와드리겠습니다...
```

### 그래프 시각화

```bash
uv run plot
```

터미널에 ASCII 그래프를 출력하고, 같은 디렉터리에 `graph.png`를 저장합니다.

---

## 프로젝트 구조

```
cs-langgraph/
├── pyproject.toml        # 프로젝트 설정 & 의존성
├── README.md
├── graph.png             # uv run plot 실행 시 생성
└── cs_agent/
    ├── __init__.py
    ├── agent.py          # 그래프 정의 (노드 + 엣지)
    └── main.py           # chat / plot 진입점
```
