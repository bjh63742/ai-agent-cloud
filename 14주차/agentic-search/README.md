# agentic-search

LangGraph 기반 Agentic Search 에이전트 프로젝트

## 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 패키지 매니저

## 설치

```bash
# uv 설치 (미설치 시)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치
uv sync
```

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 키를 설정합니다.

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 실행

```bash
uv run main.py
```

## 패키지 추가

```bash
uv add <패키지명>
```
