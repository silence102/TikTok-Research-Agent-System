# 기술 스택 (Tech Stack)

> TikTok Research Agent System의 기술 선택과 아키텍처

---

## 📊 전체 기술 스택 개요

```
┌─────────────────────────────────────────────────────┐
│              사용자 인터페이스 계층                 │
│         CLI (Python) / Slack Bot (선택)             │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              애플리케이션 계층                       │
│  Python 3.11 + Rich (CLI) + Anthropic + OpenAI      │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              워크플로우 자동화 계층                  │
│  n8n (Self-hosted on Docker)                        │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              데이터 계층                             │
│  Airtable (구조화) + ChromaDB (벡터, 선택)          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              외부 서비스 계층                        │
│  Apify | RSS Feeds | Claude API | OpenAI API        │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ 핵심 기술

### 1. 워크플로우 자동화

#### n8n (노코드 자동화 플랫폼)

**선택 이유**:
- ✅ 채용 필수 요건 ("n8n 워크플로우 자동화 도구에 대한 깊은 이해")
- ✅ 200+ 통합 지원 (Apify, Airtable, Claude API 모두 연동 가능)
- ✅ 크론 스케줄링 (매일 자동 실행)
- ✅ 비주얼 워크플로우 (디버깅 용이)
- ✅ Self-hosted (무료, 데이터 제어)

**버전**:
- n8n: v1.22.0 (2025년 1월 기준 최신 stable)
- 배포: Docker (docker.io/n8nio/n8n)

**사용 패턴**:
```yaml
에이전트 1 워크플로우:
  - Schedule Trigger (크론)
  - HTTP Request (Apify API)
  - Function (JavaScript 데이터 가공)
  - OpenAI Node (GPT-4o mini)
  - Airtable Node (Create)

에이전트 2 워크플로우:
  - Schedule Trigger (크론)
  - RSS Feed Read × 5 (병렬)
  - Merge Node
  - HTTP Request (Claude API)
  - Filter Node
  - Airtable Node (Create)
```

**장점**:
- GUI로 워크플로우 시각화 → 포트폴리오에 보여주기 좋음
- 에러 로깅 자동화
- Webhook 지원 (에이전트 3 연동 가능, Should-have)

**단점**:
- Self-hosted 필요 (Docker 환경 구축)
- JavaScript 함수 노드는 코딩 필요 (하지만 간단함)

---

### 2. LLM (Large Language Model) API

#### Claude 3.5 Sonnet (Anthropic)

**선택 이유**:
- ✅ 채용 필수 요건 ("다양한 LLM API 활용 경험")
- ✅ 한국어 품질 최고 (요약, 답변 생성에 적합)
- ✅ 긴 컨텍스트 (200K tokens)
- ✅ 환각 방지에 강함 (데이터 기반 답변)

**버전 및 모델**:
- Model ID: `claude-3-5-sonnet-20241022`
- API Version: `2023-06-01`

**사용 용도**:
1. **에이전트 2**: 뉴스 관련성 평가 (0-100점)
2. **에이전트 2**: 뉴스 요약 (200자 한국어)
3. **에이전트 3**: 질문 분류 (trend/research/mixed)
4. **에이전트 3**: RAG 답변 생성

**비용 (2025년 1월 기준)**:
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens
- **예상 월 비용**: $1.80 (하루 50K tokens × 30일)

**최적화 전략**:
```python
# 1. Temperature 조절
claude_client.messages.create(
    temperature=0.3,  # 일관성 필요 (분류, 요약)
    # temperature=0.7,  # 창의성 필요 (인사이트)
)

# 2. 캐싱 (같은 프롬프트 24시간 재사용)
@cache(ttl_hours=24)
def summarize_news(content):
    return claude_api_call(content)

# 3. 배치 처리 (5개씩 묶어서)
def batch_summarize(articles):
    prompt = "다음 5개 기사를 각각 요약하세요:\n\n"
    for article in articles:
        prompt += f"## 기사 {i}\n{article}\n\n"
    return claude_api_call(prompt)
```

---

#### GPT-4o mini (OpenAI)

**선택 이유**:
- ✅ 저비용 ($0.15/1M input tokens, Claude의 1/20)
- ✅ 빠른 응답 속도
- ✅ 간단한 분류 작업에 충분

**버전 및 모델**:
- Model ID: `gpt-4o-mini`
- API Version: OpenAI Python SDK v1.12.0

**사용 용도**:
1. **에이전트 1**: 틱톡 카테고리 분류 (Food, Dance, Comedy 등)

**비용 (2025년 1월 기준)**:
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens
- **예상 월 비용**: $0.02 (하루 30K tokens × 30일)

**사용 패턴**:
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "틱톡 콘텐츠 분류 전문가..."},
        {"role": "user", "content": f"해시태그: {hashtag}"}
    ],
    temperature=0.3,
    response_format={"type": "json_object"}
)
```

---

### 3. 데이터베이스

#### Airtable (구조화 데이터)

**선택 이유**:
- ✅ 스프레드시트 + 데이터베이스 하이브리드
- ✅ GUI로 데이터 확인 용이 (포트폴리오 데모에 적합)
- ✅ REST API 제공 (Python SDK: pyairtable)
- ✅ 무료 플랜 1,200 rows (30일 데이터 충분)
- ✅ n8n 공식 노드 지원

**무료 플랜 제약**:
- 1,200 rows per base
- 5 API calls/sec
- 2GB 첨부 파일

**스키마 설계**:

**테이블 1: tiktok_trends**
```javascript
{
  "id": "recABC123",
  "fields": {
    "date": "2025-01-15",
    "hashtag": "#BuldakChallenge",
    "views": 1200000,
    "posts_count": 3500,
    "trend_score": 92,
    "category": "Food & Cooking",
    "top_sounds": ["Fire Alarm Remix", "Spicy Beat"],
    "keywords": ["spicy", "challenge", "viral"],
    "engagement_rate": 0.12,
    "raw_data": "{...}"  // JSON string
  },
  "createdTime": "2025-01-15T09:05:23.000Z"
}
```

**테이블 2: research_news**
```javascript
{
  "id": "recXYZ789",
  "fields": {
    "date": "2025-01-15",
    "title": "Creator Economy in 2025",
    "source": "TechCrunch",
    "url": "https://...",
    "summary": "틱톡 샵 수수료 인하...",
    "keywords": ["monetization", "TikTok"],
    "relevance_score": 85,
    "sentiment": "Positive"
  }
}
```

**Python 연동**:
```python
from pyairtable import Api

api = Api(os.getenv('AIRTABLE_PAT'))
table = api.table(os.getenv('AIRTABLE_BASE_ID'), 'tiktok_trends')

# 조회 (날짜 필터)
records = table.all(
    formula="AND(IS_AFTER({date}, '2025-01-08'), {trend_score} > 50)",
    sort=[("trend_score", "desc")],
    max_records=10
)

# 생성
table.create({
    "date": "2025-01-15",
    "hashtag": "#BuldakChallenge",
    "views": 1200000,
    # ...
})
```

**아카이빙 전략** (1,200 rows 한도 대응):
```python
# 30일 이상 데이터 JSON 백업 후 삭제
import json
from datetime import datetime, timedelta

def archive_old_data():
    threshold = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    old_records = table.all(
        formula=f"IS_BEFORE({{date}}, '{threshold}')"
    )

    # JSON 백업
    with open(f'data/archive_{threshold}.json', 'w') as f:
        json.dump(old_records, f, indent=2)

    # Airtable 삭제
    for record in old_records:
        table.delete(record['id'])
```

---

#### ChromaDB (벡터 데이터베이스, Should-have)

**선택 이유**:
- ✅ 로컬 실행 가능 (무료)
- ✅ Python 네이티브
- ✅ 시맨틱 검색 (키워드 매칭보다 정확)

**사용 여부**:
- MVP (P0): ❌ 제외 (심플 RAG로 충분)
- 고도화 (P1): ✅ 포함

**사용 패턴 (P1 구현 시)**:
```python
import chromadb
from chromadb.utils import embedding_functions

# 초기화
client = chromadb.PersistentClient(path="./data/chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="tiktok_knowledge_base",
    embedding_function=embedding_fn
)

# 인덱싱 (Airtable 데이터)
for record in airtable_records:
    collection.add(
        documents=[format_document(record)],
        metadatas=[{"type": "trend", "date": record['date']}],
        ids=[f"trend_{record['id']}"]
    )

# 검색
results = collection.query(
    query_texts=["최근 인기 해시태그"],
    n_results=5
)
```

---

### 4. 외부 데이터 소스

#### Apify (TikTok 데이터 수집)

**선택 이유**:
- ✅ 공식 TikTok Hashtag Scraper Actor
- ✅ 안정적 (Cloudflare 우회 처리됨)
- ✅ 무료 플랜 50,000 results/월
- ✅ n8n HTTP Request로 쉽게 연동

**무료 플랜**:
- $5 월 크레딧 (약 50,000 results)
- 동시 실행: 1개
- 데이터 보관: 7일

**Actor**: `clockworks/tiktok-hashtag-scraper`
- Input: 해시태그 리스트
- Output: 게시물 메타데이터 (views, likes, comments, shares, sound 등)

**API 호출 예시**:
```bash
curl -X POST https://api.apify.com/v2/acts/clockworks~tiktok-hashtag-scraper/runs \
  -H "Authorization: Bearer ${APIFY_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "hashtags": ["buldak", "foodchallenge"],
    "resultsPerPage": 100,
    "shouldDownloadVideos": false
  }'
```

**대안 (백업 옵션)**:
- Unofficial TikTok API (Python 라이브러리: `TikTokApi`)
  - 장점: 무료
  - 단점: 불안정, IP 차단 위험

---

#### RSS Feeds (크리에이터 이코노미 뉴스)

**선택 이유**:
- ✅ 완전 무료
- ✅ 표준 포맷 (XML)
- ✅ n8n RSS Feed Read 노드 지원

**소스 5개**:

1. **TechCrunch Creator Economy**
   - URL: `https://techcrunch.com/tag/creator-economy/feed/`
   - 업데이트: 주 3-5회
   - 품질: ⭐⭐⭐⭐⭐ (업계 권위)

2. **Medium Creator Topics**
   - URL: `https://medium.com/tag/creator-economy/feed`
   - 업데이트: 매일
   - 품질: ⭐⭐⭐⭐ (다양한 관점)

3. **Google News Search**
   - URL: `https://news.google.com/rss/search?q=creator+economy&hl=en-US`
   - 업데이트: 실시간
   - 품질: ⭐⭐⭐ (다양한 출처)

4. **Substack Creator Newsletter**
   - URL: 수동 선별 (li.beehiiv.com 등)
   - 업데이트: 주 1-2회
   - 품질: ⭐⭐⭐⭐⭐ (심층 분석)

5. **Reddit r/CreatorEconomy**
   - URL: `https://www.reddit.com/r/CreatorEconomy/.rss`
   - 업데이트: 매일
   - 품질: ⭐⭐⭐ (커뮤니티 인사이트)

---

### 5. 프로그래밍 언어 및 프레임워크

#### Python 3.11

**선택 이유**:
- ✅ AI/ML 생태계 표준
- ✅ LLM API SDK 공식 지원 (anthropic, openai)
- ✅ 빠른 프로토타이핑

**주요 라이브러리**:

```python
# requirements.txt
anthropic==0.18.0           # Claude API
openai==1.12.0              # GPT API
pyairtable==2.3.0           # Airtable SDK
python-dotenv==1.0.0        # 환경 변수 관리
rich==13.7.0                # CLI 꾸미기 (색상, 테이블, 프로그레스 바)

# Should-have (P1)
chromadb==0.4.22            # 벡터 DB (시맨틱 검색)
sentence-transformers==2.3.1 # 임베딩 모델
```

**코딩 컨벤션**:
```python
# 포맷터: Black (line length 100)
# 타입 힌트 필수
from typing import List, Dict, Optional

def query_airtable(
    table: str,
    filter_formula: str,
    limit: int = 10
) -> List[Dict]:
    """Airtable 레코드 조회

    Args:
        table: 테이블 이름 (tiktok_trends 또는 research_news)
        filter_formula: Airtable formula (예: "IS_AFTER({date}, '2025-01-08')")
        limit: 최대 레코드 수

    Returns:
        레코드 리스트 [{"id": "rec...", "fields": {...}}, ...]
    """
    pass
```

---

#### Rich (CLI 라이브러리)

**선택 이유**:
- ✅ 터미널 출력 꾸미기 (색상, 테이블, 마크다운)
- ✅ 로딩 스피너 (UX 개선)
- ✅ 간단한 API

**사용 예시**:
```python
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.spinner import Spinner

console = Console()

# 마크다운 렌더링
md = Markdown(answer)
console.print(md)

# 테이블
table = Table(title="Top 3 Trends")
table.add_column("Hashtag", style="cyan")
table.add_column("Views", justify="right", style="green")
table.add_row("#BuldakChallenge", "1,200,000")
console.print(table)

# 스피너
with console.status("🔍 검색 중...", spinner="dots"):
    answer = engine.process_question(question)
```

---

## 🏗️ 시스템 아키텍처

### 전체 데이터 흐름

```
┌─────────────────────────────────────────────────────────┐
│                    사용자 (마케터)                       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  CLI (Python)               │
    │  - 질문 입력                │
    │  - 답변 출력 (Rich)         │
    └─────────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  Query Engine               │
    │  - 질문 분류 (Claude)       │
    │  - Airtable 조회            │
    │  - RAG 답변 생성 (Claude)   │
    └─────────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  Airtable                   │
    │  - tiktok_trends            │
    │  - research_news            │
    └─────────────┬───────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  에이전트 1   │   │  에이전트 2   │
│  (n8n)        │   │  (n8n)        │
│  매일 09:00   │   │  매일 10:00   │
└───────┬───────┘   └───────┬───────┘
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  Apify API    │   │  RSS Feeds    │
│  (TikTok)     │   │  (5개 소스)   │
└───────────────┘   └───────────────┘
```

### 기술 스택 맵

| 계층 | 기술 | 역할 | 비용 |
|------|------|------|------|
| **UI** | Python + Rich | CLI 인터페이스 | 무료 |
| **앱** | Python 3.11 | 비즈니스 로직 | 무료 |
| **워크플로우** | n8n (Docker) | 자동화 오케스트레이션 | 무료 |
| **LLM** | Claude 3.5 Sonnet | 요약, 답변 생성 | ~$1.8/월 |
| **LLM** | GPT-4o mini | 간단한 분류 | ~$0.02/월 |
| **DB** | Airtable | 구조화 데이터 | 무료 (1,200 rows) |
| **벡터** | ChromaDB (P1) | 시맨틱 검색 | 무료 |
| **데이터** | Apify | TikTok 수집 | $5/월 |
| **데이터** | RSS | 뉴스 수집 | 무료 |

**총 예상 비용**: 월 $7 이하

---

## 🔧 개발 환경

### 로컬 개발

```bash
# 필수 소프트웨어
- Python 3.11+
- Docker Desktop (n8n 실행용)
- Git

# 선택 (권장)
- VS Code (Python extension)
- Postman (API 테스트)
```

### 환경 변수 (.env)

```bash
# Airtable
AIRTABLE_PAT=pat.eJ1234567890abcdef...
AIRTABLE_BASE_ID=appABC123XYZ

# Apify
APIFY_API_TOKEN=apify_api_1234567890abcdef...

# LLM APIs
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...

# (선택) Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### n8n 실행 (Docker)

```bash
# 1회 실행
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 백그라운드 실행 (영구)
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 접속: http://localhost:5678
```

---

## 📦 배포 (선택, Should-have)

### n8n 클라우드 배포

**옵션 1: Railway.app**
- 무료 티어: $5 크레딧/월
- 1-click deploy
- HTTPS 자동

**옵션 2: n8n Cloud**
- 공식 호스팅
- $20/월 (Starter)
- 관리 불필요

**MVP에서는**: 로컬 실행만 (포트폴리오 증명용)

---

## 🔐 보안

### API 키 관리

```python
# ✅ 좋은 예: .env 파일 + python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

# ❌ 나쁜 예: 하드코딩
api_key = "sk-ant-api03-..."  # 절대 금지!
```

### .gitignore

```
.env
*.env
.env.local
data/
__pycache__/
*.pyc
.n8n/
node_modules/
```

---

## 🎯 기술 선택 의사결정

### 왜 이 기술을 선택했는가?

| 기술 | 대안 | 선택 이유 |
|------|------|-----------|
| **n8n** | Zapier, Make | 채용 필수 요건 + Self-hosted 무료 |
| **Claude** | GPT-4 | 한국어 품질 + 환각 방지에 강함 |
| **GPT-4o mini** | Claude Haiku | 저비용 ($0.15 vs $0.25) |
| **Airtable** | PostgreSQL | GUI 데이터 확인 + 포트폴리오 데모 용이 |
| **Apify** | 직접 크롤링 | 안정성 + Cloudflare 우회 |
| **Python** | Node.js | LLM SDK 공식 지원 + AI 생태계 |
| **Rich** | Click | 터미널 UI 꾸미기 (포트폴리오 인상) |

### 포기한 기술 (MVP에서 제외)

| 기술 | 이유 |
|------|------|
| **React/Next.js** | 웹 UI는 Should-have, CLI로 충분 |
| **PostgreSQL** | Airtable GUI가 포트폴리오에 더 적합 |
| **Redis** | 캐싱은 Python dict로 충분 (사용자 1명) |
| **FastAPI** | API 엔드포인트는 Nice-to-have |
| **Langchain** | 오버 엔지니어링, 직접 구현이 더 심플 |

---

## 📊 성능 및 제약 사항

### API 한도

| API | 무료 한도 | 예상 사용량 | 여유율 |
|-----|-----------|-------------|--------|
| Apify | 50,000 results/월 | 30,000 results/월 | 40% |
| Claude | Pay-as-you-go | 1.5M tokens/월 | N/A |
| OpenAI | Pay-as-you-go | 150K tokens/월 | N/A |
| Airtable | 1,200 rows | 300 rows/월 | 75% |

### 응답 시간 목표

| 기능 | 목표 | 예상 |
|------|------|------|
| 에이전트 1 전체 실행 | 10분 이내 | 5-8분 |
| 에이전트 2 전체 실행 | 15분 이내 | 10-12분 |
| 에이전트 3 질의응답 | 10초 이내 | 8-12초 |

---

**🎯 기술 스택 요약: 채용 요건 충족 + 빠른 프로토타이핑 + 저비용**
