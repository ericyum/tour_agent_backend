# Tour Agent Backend

FestMoment 백엔드 - FastAPI 기반 AI 축제 가이드 서비스

## Quick Start

```bash
# 1. Clone all three projects in the same directory
git clone <frontend-repo> tour_agent_frontend
git clone <backend-repo> tour_agent_backend
git clone <database-repo> tour_agent_database

# 2. Install dependencies
cd tour_agent_backend
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env and add your API keys (GOOGLE_API_KEY, OPENAI_API_KEY, NAVER_CLIENT_ID, etc.)

# 4. Run the server
python api_server.py

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

## 기술 스택

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **AI/ML**: LangChain, LangGraph, OpenAI, Google Generative AI
- **Database**: SQLite
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: Selenium, Playwright
- **Visualization**: Matplotlib, WordCloud, Pillow

## 프로젝트 구조 (Clean Architecture)

```
tour_agent_backend/
├── src/                     # 소스 코드 (Clean Architecture)
│   ├── application/         # 애플리케이션 레이어
│   │   ├── agents/         # AI 에이전트 (LangGraph)
│   │   ├── services/       # 비즈니스 서비스
│   │   ├── supervisors/    # 에이전트 코디네이터
│   │   └── use_cases/      # 유즈케이스 구현
│   ├── domain/             # 도메인 레이어
│   │   └── knowledge_base.py
│   └── infrastructure/     # 인프라 레이어
│       ├── config/         # 설정 관리
│       ├── persistence/    # 데이터베이스 계층
│       ├── external_services/  # 외부 API 연동
│       └── reporting/      # 리포팅 및 시각화
│
├── dic/                    # 감성 분석용 사전 파일
│   ├── adjectives.csv      # 형용사 사전
│   ├── adverbs.csv         # 부사 사전
│   ├── amplifiers.csv      # 강화어
│   ├── downtoners.csv      # 약화어
│   ├── idioms.csv          # 관용구
│   ├── negators.csv        # 부정어
│   └── sentiment_nouns.csv # 감성 명사
│
├── temp_img/               # 임시 이미지 저장 (자동 생성)
├── api_server.py           # FastAPI 서버 진입점
├── requirements.txt        # Python 의존성
├── .env.example            # 환경 변수 템플릿
└── .env                    # 환경 변수 (Git 제외)
```

**참고**: `assets/`와 `best_images_and_icons/` 폴더는 `tour_agent_database` 프로젝트에 있습니다.

## 설치 및 실행

### 필수 요구사항

- Python 3.9 이상
- 별도의 Database 프로젝트 설치 필요

### 프로젝트 Clone

**중요**: 3개의 프로젝트를 모두 같은 부모 디렉토리에 clone 하세요.

```bash
# 같은 디렉토리에 3개 프로젝트 clone
cd /your/projects/folder

git clone <frontend-repo-url> tour_agent_frontend
git clone <backend-repo-url> tour_agent_backend
git clone <database-repo-url> tour_agent_database
```

올바른 디렉토리 구조:
```
/your/projects/folder/
├── tour_agent_frontend/
├── tour_agent_backend/
└── tour_agent_database/
```

### 설치

```bash
cd tour_agent_backend
pip install -r requirements.txt
```

### 환경 변수 설정

1. `.env.example` 파일을 `.env`로 복사:
```bash
cp .env.example .env
```

2. `.env` 파일을 편집하여 필요한 API 키 입력:

```env
# AI Models (Required)
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key

# Naver API (Required for review analysis)
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# Database Path (Optional - auto-detected by default)
# DATABASE_PATH=/custom/path/to/tour_agent_database
```

**데이터베이스 경로 설정**:
- 기본적으로 형제 디렉토리 `../tour_agent_database`를 자동으로 찾습니다
- 다른 위치에 설치한 경우에만 `DATABASE_PATH` 환경 변수를 설정하세요

### 서버 실행

```bash
python api_server.py
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

### API 문서

서버 실행 후 다음 주소에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 주요 기능

### AI 에이전트
- **DB 검색 에이전트**: 축제, 시설, 코스 검색
- **네이버 리뷰 에이전트**: 블로그 리뷰 수집 및 분석
- **코스 검증 에이전트**: 여행 코스 최적화
- **주의사항 에이전트**: AI 기반 주의사항 생성

### 주요 API 엔드포인트
- `POST /api/festivals/search` - 축제 검색
- `GET /api/festivals/{festival_name}` - 축제 상세 정보
- `GET /api/festivals/{festival_name}/sentiment` - 감성 분석
- `GET /api/festivals/{festival_name}/trend` - 트렌드 분석
- `POST /api/festivals/ranking` - 축제 랭킹
- `POST /api/course/validate` - 코스 검증
- `POST /api/nearby/search` - 주변 검색

## 데이터베이스 연결

이 백엔드는 별도의 Database 프로젝트를 참조합니다:

1. `tour_agent_database` 프로젝트가 설치되어 있어야 합니다
2. `.env` 파일에 `DATABASE_PATH` 환경 변수 설정 필요
3. 데이터베이스 초기화는 서버 시작 시 자동으로 수행됩니다

## 개발 가이드

### 새로운 AI 에이전트 추가

1. `src/application/agents/`에 새 에이전트 파일 생성
2. LangGraph를 사용하여 상태 머신 정의
3. `api_server.py`에 엔드포인트 추가

### 새로운 Use Case 추가

1. `src/application/use_cases/`에 새 유즈케이스 파일 생성
2. 필요한 서비스와 에이전트 주입
3. 비즈니스 로직 구현

## 관련 프로젝트

- [Frontend](../tour_agent_frontend) - React 기반 웹 인터페이스
- [Database](../tour_agent_database) - 데이터베이스 및 데이터 파일

## 트러블슈팅

### 데이터베이스 연결 오류
- `DATABASE_PATH` 환경 변수가 올바르게 설정되었는지 확인
- `tour_agent_database` 프로젝트가 존재하는지 확인

### API 키 오류
- `.env` 파일에 모든 필수 API 키가 설정되었는지 확인
- API 키의 유효성 확인
