# 튜토리얼 (Tutorial)

> 처음 시작하는 사람을 위한 단계별 가이드

---

## 🎯 이 튜토리얼의 목표

이 튜토리얼을 완료하면:
- ✅ 로컬 환경에서 TikTok Research Agent System을 실행할 수 있습니다
- ✅ 3개 에이전트가 모두 작동하는지 확인할 수 있습니다
- ✅ CLI로 질문하고 답변을 받을 수 있습니다
- ✅ 바이브코딩 원칙을 이해하고 CLAUDE.md를 활용할 수 있습니다

**소요 시간**: 약 2-3시간

---

## 📋 사전 준비 (Prerequisites)

### 필수 소프트웨어

1. **Python 3.11 이상**
   ```bash
   python --version
   # Python 3.11.0 이상이어야 함
   ```

2. **Docker Desktop**
   - 다운로드: https://www.docker.com/products/docker-desktop/
   - 설치 후 실행 확인: `docker --version`

3. **Git**
   ```bash
   git --version
   ```

### 계정 생성 (무료)

1. **Airtable** (https://airtable.com/)
   - 무료 플랜으로 가입
   - 이메일 인증 완료

2. **Apify** (https://apify.com/)
   - 무료 플랜 ($5 크레딧)
   - 이메일 인증 완료

3. **Anthropic (Claude API)** (https://console.anthropic.com/)
   - 회원가입 후 API Key 발급
   - 결제 수단 등록 필요 (사용량 기반)

4. **OpenAI** (https://platform.openai.com/)
   - API Key 발급
   - 결제 수단 등록 필요

---

## 🚀 Step 1: 프로젝트 클론 및 설정 (10분)

### 1.1 GitHub 리포지토리 클론

```bash
# 원하는 폴더로 이동
cd ~/Desktop

# 클론 (본인 리포지토리 URL 사용)
git clone https://github.com/[YOUR_USERNAME]/TikTok-Research-Agent.git

# 폴더 진입
cd TikTok-Research-Agent
```

### 1.2 Python 가상환경 생성

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 활성화 확인 (프롬프트에 (venv) 표시됨)
```

### 1.3 Python 패키지 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt

# 설치 확인
pip list
# anthropic, openai, pyairtable, python-dotenv, rich 등이 보여야 함
```

---

## 🔑 Step 2: API 키 설정 (20분)

### 2.1 .env 파일 생성

```bash
# .env.example 복사
cp .env.example .env

# .env 파일 열기 (VS Code 또는 텍스트 에디터)
code .env  # 또는 notepad .env
```

### 2.2 Airtable 설정

**Personal Access Token 생성**:
1. Airtable 로그인: https://airtable.com/
2. 우측 상단 프로필 아이콘 → Account
3. 좌측 메뉴: Developer hub
4. "Create token" 클릭
5. Token name: "TikTok Research Agent"
6. Scopes 선택:
   - ✅ data.records:read
   - ✅ data.records:write
   - ✅ schema.bases:read
7. Access: "Add a base" → (나중에 생성할 Base 선택)
8. "Create token" → 토큰 복사 (한 번만 보임!)

**Base ID 확인**:
1. Airtable에서 새 Base 생성: "TikTok Research"
2. Base 열기
3. URL 확인: `https://airtable.com/[BASE_ID]/...`
4. BASE_ID 부분 복사 (app로 시작)

**.env 파일에 입력**:
```bash
AIRTABLE_PAT=pat.eJ1234567890abcdef...  # Personal Access Token
AIRTABLE_BASE_ID=appABC123XYZ           # Base ID
```

### 2.3 Apify 설정

1. Apify 로그인: https://console.apify.com/
2. 우측 상단: Settings → Integrations
3. API tokens → "Generate new token"
4. Token name: "TikTok Agent"
5. 토큰 복사

**.env 파일에 입력**:
```bash
APIFY_API_TOKEN=apify_api_1234567890abcdef...
```

### 2.4 Claude API 설정

1. Anthropic Console: https://console.anthropic.com/
2. API Keys → "Create Key"
3. Name: "TikTok Agent"
4. 토큰 복사

**.env 파일에 입력**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 2.5 OpenAI API 설정

1. OpenAI Platform: https://platform.openai.com/api-keys
2. "Create new secret key"
3. Name: "TikTok Agent"
4. 토큰 복사

**.env 파일에 입력**:
```bash
OPENAI_API_KEY=sk-proj-...
```

### 2.6 .env 파일 최종 확인

```bash
# .env 파일 예시 (실제 값으로 채워짐)
AIRTABLE_PAT=pat.eJ1234567890abcdef...
AIRTABLE_BASE_ID=appABC123XYZ
APIFY_API_TOKEN=apify_api_1234567890abcdef...
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
```

**⚠️ 주의**: .env 파일은 절대 Git에 커밋하지 마세요!

---

## 📊 Step 3: Airtable 테이블 생성 (15분)

### 3.1 tiktok_trends 테이블

1. Airtable Base "TikTok Research" 열기
2. 기본 테이블 이름 변경: "Table 1" → "tiktok_trends"
3. 필드 추가 (순서대로):

| 필드명 | 타입 | 옵션 |
|--------|------|------|
| date | Date | Date only, 필수 |
| hashtag | Single line text | 필수 |
| views | Number | Integer, 필수 |
| posts_count | Number | Integer |
| trend_score | Number | Integer, 0-100 |
| category | Single select | Food & Cooking, Dance & Music, Comedy, Beauty, Education, Lifestyle, Challenge, Other |
| top_sounds | Long text | - |
| keywords | Multiple select | - |
| engagement_rate | Number | Decimal (0.00) |
| raw_data | Long text | - |

4. Grid View 정렬: date (Descending)

### 3.2 research_news 테이블

1. "+" 버튼 → "Create table" → "research_news"
2. 필드 추가:

| 필드명 | 타입 | 옵션 |
|--------|------|------|
| date | Date | Date only, 필수 |
| title | Single line text | 필수 |
| source | Single select | TechCrunch, Medium, Google News, Substack, Reddit |
| url | URL | - |
| summary | Long text | - |
| keywords | Multiple select | - |
| relevance_score | Number | Integer, 0-100 |
| sentiment | Single select | Positive, Neutral, Negative |

3. Grid View 정렬: date (Descending)

### 3.3 Airtable 연동 테스트

```bash
# Python 스크립트 실행
python scripts/test_airtable.py

# 출력 예시:
# ✅ Airtable 연결 성공!
# ✅ tiktok_trends 테이블 접근 가능
# ✅ research_news 테이블 접근 가능
```

---

## 🤖 Step 4: n8n 설정 및 에이전트 1 실행 (30분)

### 4.1 n8n Docker 실행

```bash
# n8n 컨테이너 실행
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 실행 확인
docker ps
# n8n 컨테이너가 "Up" 상태여야 함

# 브라우저에서 접속
# http://localhost:5678
```

### 4.2 n8n 초기 설정

1. 브라우저에서 http://localhost:5678 열기
2. Owner account 생성:
   - Email: (본인 이메일)
   - Password: (안전한 비밀번호)
3. "Get started" 클릭

### 4.3 Credentials 추가

**Airtable**:
1. 좌측 메뉴: Credentials → "+ Add Credential"
2. "Airtable API" 검색
3. Personal Access Token: (your token)
4. "Save" → "Test" (성공 확인)

**Apify**:
1. "+ Add Credential" → "Apify API"
2. API Token: (your token)
3. "Save" → "Test"

**OpenAI**:
1. "+ Add Credential" → "OpenAI API"
2. API Key: (your key)
3. "Save"

**Anthropic Claude (HTTP Header Auth)**:
1. "+ Add Credential" → "Header Auth"
2. Name: "Anthropic Claude"
3. Header Name: `x-api-key`
4. Value: (your claude api key)
5. "Save"

### 4.4 에이전트 1 워크플로우 임포트

1. 좌측 메뉴: Workflows
2. "+ Add workflow" → "Import from File"
3. 파일 선택: `n8n-workflows/agent1-tiktok-trend-collector.json`
4. "Import"

### 4.5 에이전트 1 수동 실행 (테스트)

1. 워크플로우 열기: "Agent 1 - TikTok Trend Collector"
2. 각 노드 클릭하여 Credentials 연결 확인
3. 우측 상단: "Execute Workflow" (수동 실행)
4. 진행 상황 확인 (각 노드 초록색으로 변함)
5. 완료 후 Airtable 확인:
   - tiktok_trends 테이블에 10개 rows 생성되어야 함

**⏱️ 예상 소요 시간**: 5-8분

### 4.6 크론 스케줄 활성화

1. "Schedule Trigger" 노드 클릭
2. Cron Expression: `0 9 * * *` (매일 09:00)
3. 우측 상단: "Active" 토글 ON

---

## 📰 Step 5: 에이전트 2 실행 (20분)

### 5.1 워크플로우 임포트

1. Workflows → "+ Add workflow" → "Import from File"
2. 파일: `n8n-workflows/agent2-research-collector.json`
3. "Import"

### 5.2 RSS 소스 확인

1. 워크플로우 열기: "Agent 2 - Research Collector"
2. "RSS Feed Read" 노드 5개 확인:
   - TechCrunch
   - Medium
   - Google News
   - Substack
   - Reddit

### 5.3 수동 실행

1. "Execute Workflow" 클릭
2. 진행 상황 확인 (10-12분 소요)
3. Airtable 확인:
   - research_news 테이블에 5-10개 rows

### 5.4 크론 스케줄 활성화

1. "Schedule Trigger" 노드: `0 10 * * *` (매일 10:00)
2. "Active" 토글 ON

---

## 💬 Step 6: 에이전트 3 CLI 실행 (15분)

### 6.1 CLI 실행

```bash
# Python 가상환경 활성화 확인 (venv)
cd TikTok-Research-Agent

# CLI 실행
python src/agent3/cli.py

# 출력:
# 🤖 틱톡 리서치 에이전트에 오신 것을 환영합니다!
#
# 💡 샘플 질문:
#   - 최근 1주일 가장 핫한 해시태그는?
#   - 크리에이터 이코노미 최신 트렌드는?
#
# 질문을 입력하세요 (종료: exit):
# > _
```

### 6.2 샘플 질문 테스트

**질문 1**: 트렌드 조회
```
> 최근 1주일 가장 핫한 해시태그는?

🔍 검색 중...
📊 7일 간 데이터 조회 완료

✨ 답변:
최근 1주일 가장 핫한 해시태그 Top 3:

1. #BuldakChallenge (1,200,000 뷰)
   - 트렌드 점수: 92/100
   - 카테고리: Food & Cooking
   ...

📎 출처: Airtable (7 records)
[실행 시간: 8.2초]

> _
```

**질문 2**: 리서치 조회
```
> 크리에이터 이코노미 최신 트렌드는?

🔍 검색 중...
📰 research_news 테이블 최근 7일 데이터 분석

✨ 답변:
1️⃣ 마이크로 인플루언서 부상
   - TikTok Shop 수수료 인하
   ...

📎 출처: TechCrunch (1/12), The Information (1/10)
[실행 시간: 10.5초]

> _
```

**질문 3**: 종료
```
> exit

👋 감사합니다!
```

### 6.3 성능 확인

- [ ] 평균 응답 시간 10초 이내
- [ ] 답변에 출처 포함
- [ ] 환각 없음 (데이터 기반 답변만)

---

## 📚 Step 7: CLAUDE.md 활용법 (10분)

### 7.1 CLAUDE.md 읽기

```bash
# CLAUDE.md 파일 열기
code CLAUDE.md  # 또는 cat CLAUDE.md
```

**구조 이해**:
- **프로젝트 개요 (20줄)**: 빠른 파악
- **코딩 컨벤션 (50줄)**: 수정 시 규칙
- **필수 체크사항 (30줄)**: 보안, 성능, 에러 처리
- **자주 하는 작업 (50줄)**: 실전 가이드
- **어펜딕스 (50줄)**: 상세 문서 링크

### 7.2 바이브코딩 원칙 확인

**맥도날드 시스템**:
- 본사 (CLAUDE.md 200줄): ✅ 완성
- 지점장 (나): 의도와 의사결정 기록
- 알바 (AI): 실행

**핵심 원칙**:
1. 200줄 이내 가이드 (컨텍스트 최소화)
2. 도메인별 문서 분리 (docs/)
3. 작동하는 프로토타입 우선

### 7.3 문서 네비게이션

```bash
# 도메인별 상세 문서
ls docs/

# 출력:
# Ideation.md      (왜? - 아이디어 발상)
# PRD.md           (무엇? - 제품 요구사항)
# Tasks.md         (언제? - 작업 계획)
# TechStack.md     (어떻게? - 기술 스택)
# Tutorial.md      (현재 읽는 중!)
```

---

## 🎯 Step 8: 데모 시나리오 실행 (15분)

### 8.1 샘플 질문 20개

```bash
# 샘플 질문 파일 확인
cat demo/sample_questions.md

# CLI로 순서대로 테스트
python src/agent3/cli.py
```

**샘플 질문 예시**:
1. 최근 1주일 가장 핫한 해시태그는?
2. #BuldakChallenge 트렌드 분석해줘
3. 크리에이터 이코노미 최신 트렌드는?
4. 마이크로 인플루언서 관련 뉴스는?
5. 틱톡 트렌드와 업계 뉴스를 연결해서 설명해줘
...

### 8.2 정확도 측정

```bash
# 20개 질문 테스트 후
정답: 17개
정확도: 17/20 = 85% ✅ (목표 80% 달성!)
```

### 8.3 스크린샷 확인

```bash
# 데모 스크린샷 폴더
ls demo/screenshots/

# 7장 확인:
# 1. cli_welcome.png
# 2. cli_question_trend.png
# 3. cli_question_research.png
# 4. n8n_agent1.png
# 5. n8n_agent2.png
# 6. airtable_trends.png
# 7. airtable_research.png
```

---

## ✅ Step 9: 최종 점검 (10분)

### 9.1 체크리스트

**환경 구축**:
- [ ] Python 가상환경 작동
- [ ] .env 파일 설정 완료
- [ ] Airtable 테이블 2개 생성

**에이전트 1**:
- [ ] n8n 워크플로우 임포트
- [ ] 수동 실행 성공
- [ ] Airtable에 데이터 10+ rows
- [ ] 크론 스케줄 활성화

**에이전트 2**:
- [ ] n8n 워크플로우 임포트
- [ ] 수동 실행 성공
- [ ] Airtable에 뉴스 5+ rows
- [ ] 크론 스케줄 활성화

**에이전트 3**:
- [ ] CLI 실행 가능
- [ ] 샘플 질문 5개 테스트
- [ ] 평균 응답 시간 10초 이내
- [ ] 정확도 80% 이상

**문서**:
- [ ] CLAUDE.md 읽음 (200줄)
- [ ] docs/ 폴더 문서 5개 확인
- [ ] 바이브코딩 원칙 이해

### 9.2 트러블슈팅

**문제 1**: n8n 실행 안 됨
```bash
# Docker 재시작
docker restart n8n

# 로그 확인
docker logs n8n

# 포트 충돌 확인
lsof -i :5678  # Mac/Linux
netstat -ano | findstr :5678  # Windows
```

**문제 2**: Airtable 연결 실패
```bash
# .env 파일 확인
cat .env | grep AIRTABLE

# Personal Access Token 재발급
# Base ID 재확인
```

**문제 3**: Claude API 에러
```python
# anthropic 라이브러리 버전 확인
pip show anthropic

# 최신 버전으로 업데이트
pip install --upgrade anthropic
```

**문제 4**: CLI 느림
```python
# Airtable 데이터 확인 (너무 많으면 느림)
# 30일 이상 데이터 아카이빙:
python scripts/archive_old_data.py
```

---

## 🎓 Step 10: 다음 단계 (선택)

### 10.1 Should-have 기능 추가

**ChromaDB 벡터 검색** (P1):
```bash
pip install chromadb sentence-transformers

python scripts/import_to_chromadb.py --full-reindex
```

**Slack 통합** (P1):
1. Slack Webhook URL 생성
2. .env 파일에 추가
3. n8n에 Slack 노드 추가

### 10.2 포트폴리오 강화

**데모 영상 제작**:
- OBS Studio로 화면 녹화
- 3-5분 시연 영상
- YouTube 또는 Loom 업로드

**블로그 포스팅**:
- Medium 또는 velog
- "바이브코딩으로 틱톡 리서치 에이전트 만들기"
- 기술 스택, 배운 점, 결과

### 10.3 커뮤니티 공유

- GitHub 리포지토리 공개
- LinkedIn 포스팅
- n8n 커뮤니티 공유

---

## 🎉 축하합니다!

TikTok Research Agent System을 성공적으로 실행했습니다!

**달성한 것**:
- ✅ 3개 에이전트 모두 작동
- ✅ 자동 데이터 수집 (매일 09:00, 10:00)
- ✅ CLI 질의응답 가능
- ✅ 바이브코딩 원칙 이해

**다음 목표**:
- 🎯 삼양식품 DXT팀 채용 지원
- 🎯 포트폴리오 강화 (데모 영상, 블로그)
- 🎯 Should-have 기능 추가 (P1)

---

## 📞 도움이 필요하신가요?

**문서 참조**:
- [PRD.md](./PRD.md) - 제품 요구사항
- [TechStack.md](./TechStack.md) - 기술 스택
- [Tasks.md](./Tasks.md) - 작업 계획
- [CLAUDE.md](../CLAUDE.md) - AI 작업 가이드

**커뮤니티**:
- n8n Community: https://community.n8n.io/
- Anthropic Discord: https://discord.gg/anthropic

**Issue 보고**:
- GitHub Issues: (본인 리포지토리 URL)

---

*이 튜토리얼은 "작동하는 에이전트"를 직접 경험하는 것을 목표로 합니다. 즐거운 코딩 되세요! 🚀*
