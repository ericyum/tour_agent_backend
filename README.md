# FestMoment Backend 🤖✨

> "축제의 순간을 AI로 재해석하다"
>
> **Team FestMoment** | 염정운, 최가윤

**FestMoment Backend**는 LLM과 Vision 모델을 활용한 AI 축제 가이드 서비스의 핵심 엔진입니다. 블로그 후기, 검색량 트렌드, 현장 이미지 등 비정형 데이터 속에 담긴 **감성**을 AI로 분석하고, 사용자에게 축제의 '순간'을 생생하게 전달합니다.

---

## 📑 목차

1. [핵심 기능](#-핵심-기능)
2. [기술 아키텍처](#-기술-아키텍처)
3. [기술 스택](#-기술-스택)
4. [프로젝트 구조](#-프로젝트-구조)
5. [Quick Start](#-quick-start)
6. [상세 설치 가이드](#-상세-설치-가이드)
7. [API 문서](#-api-문서)
8. [개발 가이드](#-개발-가이드)

---

## 🌟 핵심 기능

### 1. AI 심층 분석 (네이버 데이터 기반)

- **블로그 리뷰 AI 요약**: Gemini LLM이 네이버 블로그 후기를 실시간 분석하여 **장점, 단점, 방문 꿀팁** 제공
- **다차원 감성 분석**: 자체 감성 사전(규칙 기반) + Gemini(LLM 동적 분석) 하이브리드 방식
- **이상치 필터링**: IQR(사분위수 범위)로 극단적 리뷰 필터링, 객관적 평점 도출
- **검색량 트렌드**: Naver DataLab API 연간 검색량 추이 시각화
- **테마별 워드클라우드**: 7가지 축제 테마별 키워드 시각화

### 2. AI 렌더링 및 시각화

- **베스트 포토 자동 선정**: Gemini Vision이 블로그 이미지 분석, 대표 사진 추출
- **영화 포스터 스타일 렌더링**: AI가 축제 이미지를 감성적 포스터로 재창조
- **계절/시간대별 렌더링**: 봄/여름/가을/겨울, 낮/밤 장면을 AI로 재구성
- **AI 아이콘 생성**: 축제 핵심 상징을 담은 아이콘 자동 생성

### 3. 검색 및 개인 맞춤형 가이드

- **계층적 카테고리 검색**: 지역별, 테마별, 기간별 다각적 필터링
- **객관적 축제 랭킹**: 평점 + 리뷰 수 + 검색량 종합 분석
- **AI 여행 코스 검증**: 이동 시간, 동선 현실성 검토 및 최적화 제안
- **지도 기반 주변 추천**: 반경 내 추천 코스 및 문화시설 정보

---

## 🏗️ 기술 아키텍처

**LangGraph 기반 계층적 에이전트 아키텍처**로 복잡한 AI 워크플로우를 유연하게 관리합니다.

### 아키텍처 계층

```
┌─────────────────────────────────────────────────┐
│  Frontend (React)                               │
│  ↓ HTTP API Requests                            │
├─────────────────────────────────────────────────┤
│  FastAPI Server (api_server.py)                 │
│  ↓ Route to Use Cases                           │
├─────────────────────────────────────────────────┤
│  Application Layer                              │
│  ├─ Use Cases (비즈니스 로직)                    │
│  ├─ Supervisors (에이전트 코디네이터)            │
│  └─ Agents (LangGraph 노드)                     │
│     ├─ DB Search Agent                          │
│     ├─ Naver Review Agent                       │
│     ├─ Course Validation Agent                  │
│     └─ Rendering Agent                          │
│  ↓                                               │
├─────────────────────────────────────────────────┤
│  Infrastructure Layer                           │
│  ├─ External Services (Naver, Google APIs)      │
│  ├─ Persistence (SQLite via Database Project)   │
│  ├─ LLM Client (Gemini)                         │
│  └─ Reporting (Charts, Wordclouds)              │
└─────────────────────────────────────────────────┘
```

### LangGraph 워크플로우

- **자체 교정 루프**: LLM 요약 → 규칙 기반 점수 → 불일치 시 피드백 → 재학습
- **병렬 처리**: 다수 블로그 리뷰 동시 분석으로 성능 최적화
- **동적 학습**: 미등록 감성 단어 발견 시 자동으로 사전에 추가

---

## 🛠️ 기술 스택

### Core Technologies
- **Language**: Python 3.9+
- **Web Framework**: FastAPI
- **AI Framework**: LangGraph (계층적 에이전트)
- **LLM**: Google Gemini (Pro, Flash, Vision)

### AI & Data Processing
- **NLP**: Konlpy (형태소 분석), Pandas
- **Visualization**: Matplotlib, WordCloud, Pillow
- **Web Scraping**: Playwright, Selenium

### External APIs
- **축제 정보**: 한국관광공사 TourAPI
- **리뷰/트렌드**: Naver Search API, Naver DataLab API
- **지도/위치**: Google Static Maps API
- **이미지 생성**: Google Gemini Vision

### Database
- **SQLite**: 축제, 문화시설, 여행코스 데이터
- **자체 사전**: 감성 분석용 형용사/부사/명사 사전 (`dic/`)

---

## 📁 프로젝트 구조

**Clean Architecture** 기반으로 계층을 명확히 분리했습니다.

```
tour_agent_backend/
├── src/                     # 소스 코드
│   ├── application/         # 🟣 Application Layer
│   │   ├── agents/         # LangGraph 에이전트 노드
│   │   │   ├── db_search/
│   │   │   ├── naver_review/
│   │   │   ├── course_validation/
│   │   │   └── precaution_agent.py
│   │   ├── core/           # LangGraph 핵심 (State, Graph)
│   │   ├── supervisors/    # 에이전트 코디네이터
│   │   ├── services/       # 비즈니스 서비스
│   │   └── use_cases/      # 복잡한 비즈니스 로직
│   │       ├── sentiment_analysis_use_case.py
│   │       ├── ranking_use_case.py
│   │       ├── rendering_use_case.py
│   │       └── analysis_use_case.py
│   │
│   ├── domain/             # 🟡 Domain Layer
│   │   └── knowledge_base.py # 감성 사전 로딩
│   │
│   └── infrastructure/     # 🟢 Infrastructure Layer
│       ├── config/         # 환경 설정
│       ├── persistence/    # DB 연결 (Database 프로젝트 참조)
│       ├── external_services/  # 외부 API 연동
│       ├── reporting/      # 시각화 (Charts, Wordclouds)
│       ├── llm_client.py   # LLM 클라이언트
│       └── dynamic_scorer.py # 동적 감성 점수
│
├── dic/                    # 감성 분석용 사전
│   ├── adjectives.csv
│   ├── adverbs.csv
│   ├── amplifiers.csv
│   ├── downtoners.csv
│   ├── idioms.csv
│   ├── negators.csv
│   └── sentiment_nouns.csv
│
├── temp_img/               # 임시 이미지 저장
├── api_server.py           # FastAPI 서버 진입점
├── requirements.txt
├── .env.example
└── .env                    # 환경 변수 (Git 제외)
```

**참고**: `assets/`, `best_images_and_icons/` 폴더는 `tour_agent_database` 프로젝트에 있습니다.

---

## 🚀 Quick Start

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
# Edit .env and add your API keys:
#   - GOOGLE_API_KEY (required)
#   - OPENAI_API_KEY (required)
#   - NAVER_CLIENT_ID, NAVER_CLIENT_SECRET (required)
#   - NAVER_TREND_CLIENT_ID, NAVER_TREND_CLIENT_SECRET (optional)

# 4. Run the server
python api_server.py

# ✅ Server starts at http://localhost:8000
# 📖 API docs at http://localhost:8000/docs
```

---

## 📚 상세 설치 가이드

### 필수 요구사항

- **Python 3.9 이상**
- **별도 Database 프로젝트 필요** (자동 경로 탐지)

### 프로젝트 Clone

**⚠️ 중요**: 3개 프로젝트를 모두 **같은 부모 디렉토리**에 clone 하세요.

```bash
cd /your/projects/folder

git clone <frontend-repo-url> tour_agent_frontend
git clone <backend-repo-url> tour_agent_backend
git clone <database-repo-url> tour_agent_database
```

**올바른 디렉토리 구조**:
```
/your/projects/folder/
├── tour_agent_frontend/
├── tour_agent_backend/  ← 이 프로젝트
└── tour_agent_database/
```

### 환경 변수 설정

1. `.env.example`을 `.env`로 복사:
```bash
cp .env.example .env
```

2. `.env` 파일 편집 (필수 항목):

```env
# AI Models (Required)
GOOGLE_API_KEY=your_google_gemini_api_key
OPENAI_API_KEY=your_openai_api_key

# Naver API (Required for review analysis)
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# Naver Trend (Optional)
NAVER_TREND_CLIENT_ID=your_naver_trend_client_id
NAVER_TREND_CLIENT_SECRET=your_naver_trend_client_secret

# Database Path (Optional - auto-detected by default)
# DATABASE_PATH=/custom/path/to/tour_agent_database
```

**데이터베이스 경로**:
- 기본적으로 형제 디렉토리 `../tour_agent_database`를 자동 탐지
- 다른 위치에 설치한 경우에만 `DATABASE_PATH` 설정 필요

### 서버 실행

```bash
python api_server.py
```

서버 시작 시 다음 메시지 확인:
```
[Database] Using DATABASE_PATH: /path/to/tour_agent_database
[Loader] Using DATABASE_PATH: /path/to/tour_agent_database
✅ FestMoment API Server Started (Database: /path/to/tour_agent_database)
```

---

## 📖 API 문서

서버 실행 후 자동 생성된 API 문서 확인:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 엔드포인트

#### 축제 검색 및 정보
- `POST /api/festivals/search` - 축제 검색 (필터링)
- `GET /api/festivals/{festival_name}` - 축제 상세 정보
- `GET /api/config/areas` - 지역 목록
- `GET /api/config/categories` - 카테고리 목록

#### AI 분석
- `GET /api/festivals/{festival_name}/sentiment` - 감성 분석
- `GET /api/festivals/{festival_name}/trend` - 트렌드 분석
- `GET /api/festivals/{festival_name}/wordcloud` - 워드클라우드
- `GET /api/festivals/{festival_name}/precautions` - AI 주의사항

#### AI 렌더링
- `POST /api/festivals/{festival_name}/render` - AI 이미지 생성
- `GET /api/festivals/{festival_name}/images` - 베스트 포토

#### 랭킹 및 코스
- `POST /api/festivals/ranking` - 축제 랭킹
- `POST /api/course/validate` - 여행 코스 검증
- `POST /api/nearby/search` - 주변 추천

---

## 👨‍💻 개발 가이드

### 새로운 AI 에이전트 추가

1. `src/application/agents/`에 새 에이전트 파일 생성
2. LangGraph State와 노드 정의:

```python
from langgraph.graph import StateGraph
from src.application.core.state import YourState

def your_agent_node(state: YourState) -> YourState:
    # AI 로직 구현
    return state

# Graph 생성
graph = StateGraph(YourState)
graph.add_node("process", your_agent_node)
graph.set_entry_point("process")
graph.set_finish_point("process")
your_agent_graph = graph.compile()
```

3. `api_server.py`에 엔드포인트 추가

### 새로운 Use Case 추가

1. `src/application/use_cases/`에 새 유즈케이스 생성
2. 필요한 Agent/Service 주입:

```python
class YourUseCase:
    def __init__(self, your_agent, your_service):
        self.agent = your_agent
        self.service = your_service

    async def execute(self, input_data):
        # 비즈니스 로직
        result = self.agent.invoke({"input": input_data})
        return self.service.process(result)
```

3. `api_server.py`에서 초기화 및 사용

---

## 🔧 트러블슈팅

### 데이터베이스 연결 오류
```
Error: [WinError 3] 지정된 경로를 찾을 수 없습니다: '...\festivals'
```
**해결**:
- `tour_agent_database` 프로젝트가 형제 디렉토리에 있는지 확인
- 서버 시작 로그에서 `DATABASE_PATH` 확인

### API 키 오류
```
Error: Invalid API key
```
**해결**:
- `.env` 파일에 올바른 API 키 설정 확인
- API 키 유효성 확인 (Google Cloud Console, Naver Developers)

### 이미지 생성 실패
```
Warning: best_images_and_icons not found
```
**해결**:
- `tour_agent_database` 프로젝트에 `best_images_and_icons/` 폴더 존재 확인
- `assets/` 폴더도 Database 프로젝트에 있어야 함

---

## 🤝 관련 프로젝트

- [**Frontend**](../tour_agent_frontend) - React 기반 웹 인터페이스
- [**Database**](../tour_agent_database) - 데이터베이스 및 정적 리소스

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 개발되었습니다.

---

## 👥 개발팀

**Team FestMoment**
- 염정운
- 최가윤

**문의**: [GitHub Issues](https://github.com/your-repo/issues)

---

**FestMoment** - AI로 축제의 감성을 재해석합니다 ✨
