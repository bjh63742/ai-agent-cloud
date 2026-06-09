# AI Agent Cloud

개발 환경 설정 가이드

---

## 목차

| #   | 주제                                               | 설명                        |
| --- | -------------------------------------------------- | --------------------------- |
| 1   | [Git 설치](docs/git.md)                            | Git 설치 및 초기 설정       |
| 2   | [GitHub Desktop 설치](docs/github-desktop.md)      | GUI 기반 Git 클라이언트     |
| 3   | [Node.js 설치](docs/nodejs.md)                     | Node.js 및 npm 설치         |
| 4   | [Python 설치](docs/python.md)                      | Python 및 pip 설치          |
| 5   | [uv (Python 패키지 매니저)](docs/uv.md)            | 초고속 Python 패키지 매니저 |
| 6   | [VS Code 확장 프로그램](docs/vscode-extensions.md) | 권장 VS Code 확장 프로그램  |
| 7   | [Ollama 설치](docs/ollama.md)                      | 로컬 LLM 실행 환경          |
| 8   | [Docker Desktop 설치](docs/docker.md)              | 컨테이너 기반 개발 환경     |

---

## Docker로 개발 환경 실행하기

MySQL, PostgreSQL, Redis, Adminer를 Docker로 한 번에 실행할 수 있습니다.

### 사전 준비

[Docker Desktop](docs/docker.md)이 설치되어 있어야 합니다.

### 실행 방법

#### Mac (Apple Silicon — M1/M2/M3/M4)

```bash
docker compose -f docker/docker-compose.mac.yml up -d
```

#### Windows (또는 Mac Intel)

```bash
docker compose -f docker/docker-compose.windows.yml up -d
```

### 종료 방법

```bash
# Mac
docker compose -f docker/docker-compose.mac.yml down

# Windows
docker compose -f docker/docker-compose.windows.yml down
```

### 접속 정보

| 서비스 | 주소 | 기본 계정 |
| --- | --- | --- |
| Adminer (DB 관리 UI) | http://localhost:8080 | - |
| MySQL | localhost:3306 | root / password |
| PostgreSQL | localhost:5432 | postgres / password |
| Redis | localhost:6379 | - |

> **Adminer 접속 방법**: 브라우저에서 http://localhost:8080 열고, 서버에 `mysql` 또는 `postgres` 입력 후 위 계정으로 로그인
