# python-react-pat

Ollama 기반 ReAct 패턴 AI 에이전트입니다.

## 사전 준비

1. [Ollama](https://ollama.com) 설치
2. 모델 다운로드
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

## 설치

```bash
# 의존성 설치 (uv 사용)
uv sync

# 또는 pip 사용
pip install ollama
```

## 실행

```bash
uv run main.py
```

## 구조

```
main.py   # Agent 클래스 및 진입점
```

### Agent 클래스

- `__init__(system)` — 시스템 프롬프트 설정, 대화 기록 초기화
- `__call__(message)` — 메시지를 받아 응답 반환 (함수처럼 호출 가능)
- `execute()` — Ollama API 호출

```python
agent = Agent("당신은 친절한 AI입니다.")
response = agent("안녕하세요!")
print(response)
```

## 사용 모델

| 모델 | 설명 |
|---|---|
| `qwen2.5-coder:7b` | Alibaba의 코딩 특화 모델 |
