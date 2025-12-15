# PRD (Product Requirements Document)

> 제품 요구사항 정의서 - TikTok Research Agent System

---

## 📋 문서 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2025-12-15 |
| **버전** | v1.0 (MVP) |
| **작성자** | [Minseok Kim] |
| **프로젝트명** | TikTok Research Agent System |
| **목표** | 삼양식품 DXT팀 채용 포트폴리오 |

---

## 🎯 Goal (목표)

### Primary Goal

**"틱톡 트렌드 및 크리에이터 이코노미 리서치를 자동화하는 AI 에이전트 시스템 구축"**

### Business Goals

1. **시간 단축**: 마케터의 리서치 시간을 90% 단축 (2시간 → 10분)
2. **데이터 기반 의사결정**: 매일 업데이트되는 트렌드 DB 제공
3. **인사이트 도출**: LLM 기반 자동 분석 및 실행 가능한 제안

### Technical Goals

1. **n8n 워크플로우 자동화**: 3개 에이전트의 크론 스케줄링
2. **다양한 LLM API 활용**: Claude (고품질) + GPT (저비용) 혼용
3. **프롬프트 엔지니어링**: 환각 방지 + RAG 구현
4. **바이브코딩 원칙 실천**: 200줄 CLAUDE.md + 도메인별 문서 분리

### Portfolio Goals

1. **채용 필수 요건 충족**: "최근 1개월 내 직접 만든 에이전트 2개 이상"
2. **실전 역량 증명**: 작동하는 프로토타입 + 데모
3. **차별화**: 바이브코딩 방법론 이해 및 실천

---

## ❌ Non-Goal (범위 외)

### 명확히 하지 않을 것

1. **실시간 처리**
   - 이유: 배치 작업(매일 1-2회)으로 충분
   - 트레이드오프: 실시간성 포기 → 비용/복잡도 절감

2. **프로덕션 레벨 확장성**
   - 이유: 포트폴리오 증명용 (사용자 1명)
   - 트레이드오프: 확장성 포기 → 개발 속도 우선

3. **개별 크리에이터 프로파일링**
   - 이유: 트렌드 분석에 집중
   - 트레이드오프: 범위 축소 → MVP 1주일 완성

4. **유료 엔터프라이즈 API**
   - 이유: 비용 최소화 (월 $10 이하)
   - 트레이드오프: 데이터 정확성 일부 포기 → 포트폴리오에 충분

5. **영상 편집 자동화**
   - 이유: 분석만으로 충분
   - 트레이드오프: 기능 축소 → 개발 복잡도 감소

---

## 🎯 우선순위 분류

### Must-have (P0) - MVP 필수 기능

**1주일 내 반드시 구현해야 할 기능**

#### 에이전트 1: 틱톡 트렌드 자동 수집
- [ ] 매일 09:00 KST 크론 스케줄링 (n8n)
- [ ] Apify TikTok Hashtag Scraper API 연동
- [ ] 10개 해시태그 동시 수집 (buldak, foodchallenge 등)
- [ ] GPT-4o mini로 카테고리 분류 (Food, Dance, Comedy 등)
- [ ] Airtable `tiktok_trends` 테이블에 저장
- [ ] 필드: date, hashtag, views, posts_count, trend_score, category, keywords

#### 에이전트 2: 크리에이터 이코노미 뉴스 수집
- [ ] 매일 10:00 KST 크론 스케줄링 (n8n)
- [ ] 5개 RSS 피드 병렬 수집 (TechCrunch, Medium, Google News 등)
- [ ] 중복 제거 (URL + 제목 유사도)
- [ ] Claude API로 관련성 평가 (0-100점)
- [ ] relevance_score >= 70만 통과
- [ ] Claude API로 200자 이내 한국어 요약
- [ ] Airtable `research_news` 테이블에 저장

#### 에이전트 3: 통합 질의응답
- [ ] CLI 인터페이스 (Python)
- [ ] 자연어 질문 입력 받기
- [ ] Claude API로 질문 분류 (trend / research / mixed)
- [ ] Airtable 데이터 조회 (날짜 필터링)
- [ ] 컨텍스트 준비 (Top 5-10 레코드)
- [ ] Claude API로 RAG 답변 생성
- [ ] 출처 링크 포함 응답
- [ ] 평균 응답 시간 10초 이내

#### 문서화
- [ ] README.md (프로젝트 개요, 설치 가이드, 사용 예시)
- [ ] CLAUDE.md (200줄 이내 AI 작업 가이드)
- [ ] docs/PROMPTS.md (모든 프롬프트 문서화)
- [ ] demo/sample_questions.md (샘플 질문 20개)
- [ ] 스크린샷 3장 이상

#### 테스트
- [ ] 에이전트 1 수동 실행 테스트 (3회 이상)
- [ ] 에이전트 2 수동 실행 테스트 (3회 이상)
- [ ] 에이전트 3 질의응답 테스트 (5개 질문)
- [ ] 7일 연속 자동 실행 검증

---

### Should-have (P1) - 고도화 기능

**MVP 완성 후 2-3일 추가 개발**

#### 벡터 검색 (ChromaDB)
- [ ] ChromaDB 로컬 설치
- [ ] Airtable 데이터 임베딩 (Claude Embeddings API)
- [ ] 시맨틱 검색 구현
- [ ] 키워드 매칭 대비 정확도 향상 측정

#### Slack 통합
- [ ] 에이전트 1 완료 시 Slack 알림
- [ ] 에이전트 2 일일 리포트 (Top 3 뉴스)
- [ ] 에러 발생 시 Slack 알림
- [ ] Slack Bot으로 질의응답 가능

#### 주간 리포트
- [ ] 주간 트렌드 비교 (전주 대비 변화)
- [ ] 차트 생성 (matplotlib)
- [ ] PDF 리포트 자동 생성
- [ ] 이메일 발송

#### 성능 최적화
- [ ] 캐싱 구현 (동일 프롬프트 24시간 캐시)
- [ ] 배치 처리 (5개씩 묶어서 LLM 호출)
- [ ] 토큰 사용량 모니터링 대시보드

---

### Nice-to-have (P2) - 추가 개선

**시간 여유 있을 때 또는 추후 개선**

#### Streamlit Web UI
- [ ] 검색 인터페이스
- [ ] 결과 시각화 (차트, 테이블)
- [ ] 날짜 범위 필터
- [ ] Streamlit Cloud 배포

#### 트렌드 예측
- [ ] 과거 데이터 기반 회귀 분석
- [ ] 다음 주 예상 트렌드 Top 3 예측
- [ ] 신뢰도 점수 표시

#### 다국어 지원
- [ ] 영어 질문 지원
- [ ] 영어 답변 생성
- [ ] 한/영 자동 감지

#### API 엔드포인트
- [ ] FastAPI로 REST API 구축
- [ ] `/api/trends` (GET)
- [ ] `/api/research` (GET)
- [ ] `/api/ask` (POST)
- [ ] Swagger 문서

---

## 👥 사용자 여정 (User Journey)

### 페르소나: 마케팅 매니저 "지수"

**배경**:
- 삼양식품 DXT팀 마케팅 매니저
- 틱톡 트렌드 파악을 위해 매일 아침 2시간 소비
- 비기술자 (코딩 불가능)

### Scenario 1: 아침 일과 (기존 vs 개선)

#### Before (수동 리서치)

```
08:00 - 출근
08:30 - 틱톡 앱 열기
      → 인기 해시태그 10개 수동 메모
      → 조회수, 게시물 수 스프레드시트에 입력
09:00 - 구글링 "creator economy news"
      → 5-10개 기사 읽기
      → 엑셀에 요약 정리
10:30 - 리서치 완료 (2시간 소요)
10:30 - 실제 업무 시작 (늦음)
```

**문제점**:
- 반복적 작업에 시간 낭비
- 주관적 선택 (트렌드 놓칠 수 있음)
- 데이터 누적 어려움 (스프레드시트 관리 복잡)

#### After (에이전트 시스템)

```
08:00 - 출근
08:30 - CLI 실행: python agent3/cli.py
      > "최근 1주일 가장 핫한 해시태그는?"
      → 8초 만에 답변 수신 (Top 3 + 인사이트)

      > "크리에이터 이코노미 최신 트렌드는?"
      → 10초 만에 답변 수신 (뉴스 요약 + 출처)
08:40 - 리서치 완료 (10분 소요)
08:40 - 실제 업무 시작 (빠름)
```

**개선점**:
- 시간 90% 단축 (2시간 → 10분)
- 객관적 데이터 (LLM 기반 분석)
- 자동 누적 (Airtable 30일 이력)

---

### Scenario 2: 브랜드 협업 기획

**상황**: "#BuldakChallenge" 브랜디드 콘텐츠 기획 중

#### Step 1: 트렌드 확인
```
> "#BuldakChallenge 트렌드 분석해줘"

✨ 답변:
#BuldakChallenge (2025-01-15 기준)
- 조회수: 1,200,000 (전주 대비 +35%)
- 게시물 수: 3,500개
- 트렌드 점수: 92/100
- 주요 사운드: "Fire Alarm Remix"
- 참여 크리에이터: 마이크로(70%), 중형(25%), 대형(5%)

💡 인사이트:
마이크로 인플루언서(1K-10K) 참여도가 높음.
Popow 타겟층과 정확히 일치.

📎 출처: Airtable (1/15)
```

#### Step 2: 업계 트렌드 연결
```
> "마이크로 인플루언서 관련 최신 뉴스는?"

✨ 답변:
1️⃣ TikTok Shop 소규모 크리에이터 수수료 인하 (1/12)
   - 1K-50K 팔로워 수수료 15% → 10%
   - 예상 효과: 마이크로 인플루언서 수익성 개선

2️⃣ 브랜디드 콘텐츠 CPM 20% 상승 (1/10)
   - 식품 브랜드 광고비 증가 추세

📎 출처: TechCrunch, The Information
```

#### Step 3: 의사결정
```
지수의 판단:
✅ #BuldakChallenge는 마이크로 인플루언서 중심
✅ TikTok Shop 정책 변화로 수익화 기회 증가
✅ 식품 브랜드 CPM 상승 → 예산 확보 유리

→ Popow 플랫폼에 마이크로 크리에이터 온보딩 집중!
```

**결과**: 데이터 기반 의사결정 (10분) vs 직감 기반 (며칠)

---

## 🔧 기능 명세서

### 에이전트 1: 틱톡 트렌드 자동 수집

#### Input (입력)
- **트리거**: n8n Schedule Trigger (매일 09:00 KST)
- **해시태그 리스트**: 10개 고정 (설정 파일)
  ```json
  [
    "buldak", "foodchallenge", "koreanfood",
    "spicychallenge", "mukbang", "foodreview",
    "tiktokfood", "viralrecipe", "foodtrend", "trending"
  ]
  ```

#### Processing (처리)
1. **데이터 수집** (Apify API)
   - 각 해시태그별 Top 100 게시물 메타데이터
   - 필드: id, text, views, likes, comments, shares, sound

2. **데이터 정제** (n8n Function 노드)
   - 집계: 총 조회수, 게시물 수, 평균 참여율
   - 트렌드 점수 계산 (0-100):
     ```javascript
     trend_score = (
       (avg_views / 10000) * 0.4 +
       (avg_engagement * 100) * 0.3 +
       (growth_rate) * 0.3
     )
     ```

3. **카테고리 분류** (GPT-4o mini)
   - 프롬프트: "Food & Cooking, Dance, Comedy 등 8개 카테고리 분류"
   - Temperature: 0.3 (일관성)
   - 출력: JSON `{"category": "Food & Cooking", "confidence": 0.95}`

4. **키워드 추출** (Claude API)
   - 프롬프트: "마케팅 인사이트에 유용한 키워드 5-10개 추출"
   - 제외 단어: 조사, "틱톡", "챌린지" 등

#### Output (출력)
- **Airtable `tiktok_trends` 테이블에 저장**

| 필드 | 타입 | 예시 |
|------|------|------|
| date | Date | 2025-01-15 |
| hashtag | Single Line Text | #BuldakChallenge |
| views | Number | 1,200,000 |
| posts_count | Number | 3,500 |
| trend_score | Number | 92 |
| category | Single Select | Food & Cooking |
| top_sounds | Long Text (JSON) | ["Fire Alarm Remix", "Spicy Beat"] |
| keywords | Multiple Select | spicy, challenge, viral, korean |
| engagement_rate | Number | 0.12 (12%) |
| raw_data | Long Text (JSON) | {...} (디버깅용) |

#### Success Criteria (성공 기준)
- [ ] 매일 09:00 정확히 실행
- [ ] 10개 해시태그 모두 수집 (성공률 95%+)
- [ ] Airtable에 10개 row 생성
- [ ] 실행 시간 10분 이내
- [ ] 에러 발생 시 Slack 알림 (선택)

---

### 에이전트 2: 크리에이터 이코노미 뉴스 수집

#### Input (입력)
- **트리거**: n8n Schedule Trigger (매일 10:00 KST)
- **RSS 피드 소스**: 5개 URL
  1. TechCrunch Creator Economy
  2. Medium Creator Topics
  3. Google News "creator economy"
  4. Substack 선별 뉴스레터
  5. Reddit r/CreatorEconomy

#### Processing (처리)
1. **RSS 수집** (n8n RSS Feed Read 노드 × 5개 병렬)
   - 각 소스에서 최근 24시간 기사 수집
   - 필드: title, link, pubDate, description

2. **중복 제거** (n8n Function 노드)
   - URL 중복 체크
   - 제목 유사도 체크 (Levenshtein distance > 0.85면 중복)

3. **전문 가져오기** (HTTP Request)
   - Readability API 또는 직접 파싱
   - 텍스트만 추출 (HTML 태그 제거)

4. **관련성 평가** (Claude API)
   - 프롬프트: "틱톡 크리에이터 비즈니스 관련성 0-100점"
   - Temperature: 0.5
   - 출력: `{"relevance_score": 85, "reasoning": "..."}`

5. **필터링** (n8n Filter 노드)
   - relevance_score >= 70만 통과

6. **요약** (Claude API)
   - 프롬프트: "200자 이내 한국어 요약 + 실행 인사이트"
   - Temperature: 0.7
   - 출력: 구조화된 요약문

7. **키워드 추출** (Claude API)
   - 감성 분석 (Positive/Neutral/Negative)

#### Output (출력)
- **Airtable `research_news` 테이블에 저장**

| 필드 | 타입 | 예시 |
|------|------|------|
| date | Date | 2025-01-15 |
| title | Single Line Text | "Creator Economy in 2025" |
| source | Single Select | TechCrunch |
| url | URL | https://... |
| summary | Long Text | "틱톡 샵 수수료 인하..." (200자) |
| keywords | Multiple Select | monetization, TikTok, micro-influencer |
| relevance_score | Number | 85 |
| sentiment | Single Select | Positive |

#### Success Criteria (성공 기준)
- [ ] 매일 10:00 정확히 실행
- [ ] 5개 소스 모두 수집 성공
- [ ] 중복 제거 후 평균 5-10개 기사
- [ ] 모든 기사 요약 완료
- [ ] Airtable에 5+ rows 생성
- [ ] 실행 시간 15분 이내

---

### 에이전트 3: 통합 질의응답

#### Input (입력)
- **인터페이스**: CLI (Python)
- **질문 형식**: 자연어 (한국어)
- **예시**:
  - "최근 1주일 가장 핫한 해시태그는?"
  - "크리에이터 이코노미 최신 트렌드는?"
  - "#BuldakChallenge 트렌드와 업계 뉴스를 연결해서 설명해줘"

#### Processing (처리)
1. **질문 분류** (Claude API)
   - 카테고리: trend / research / mixed
   - 날짜 필터: last_7_days / last_30_days / all
   - 키워드 추출
   - 출력:
     ```json
     {
       "category": "trend",
       "date_filter": "last_7_days",
       "keywords": ["해시태그", "인기"],
       "intent": "조회수 높은 트렌드 상위 리스트"
     }
     ```

2. **데이터 조회** (Airtable API)
   - 분류에 따라 적절한 테이블 조회
   - 날짜 필터링
   - 관련성 순 정렬 (trend_score 또는 relevance_score)
   - Top 5-10 레코드 선택

3. **컨텍스트 준비** (Python Function)
   - 마크다운 포맷으로 정리:
     ```markdown
     # 틱톡 트렌드 데이터

     ## 1. #BuldakChallenge
     - 날짜: 2025-01-15
     - 조회수: 1,200,000
     - 트렌드 점수: 92/100
     ...
     ```

4. **RAG 답변 생성** (Claude API)
   - System Prompt: "데이터 기반 답변, 환각 금지"
   - User Prompt: "질문: {{question}}\n\n데이터: {{context}}"
   - Temperature: 0.3
   - Max tokens: 1024

5. **후처리** (Python Function)
   - 출처 링크 추가
   - 마크다운 포맷팅
   - 실행 시간 측정

#### Output (출력)
- **CLI 화면에 출력**
  ```
  🔍 검색 중... (2초)
  📊 7일 간 데이터 조회 완료

  ✨ 답변:
  [핵심 답변 1-2문장]

  [상세 내용 - Bullet points]

  💡 실행 인사이트: [구체적 제안]

  📎 출처: Airtable (7 records)
  [실행 시간: 8.2초]
  ```

#### Success Criteria (성공 기준)
- [ ] 자연어 질문 정확히 이해 (분류 정확도 90%+)
- [ ] 평균 응답 시간 10초 이내
- [ ] 답변에 출처 포함
- [ ] 환각 없음 (데이터 기반 답변만)
- [ ] 샘플 20개 질문 테스트 통과 (정확도 80%+)

---

## 🎨 UX 설계

### CLI 인터페이스 (MVP)

#### 시작 화면
```
$ python src/agent3/cli.py

🤖 틱톡 리서치 에이전트에 오신 것을 환영합니다!

💡 샘플 질문:
  - 최근 1주일 가장 핫한 해시태그는?
  - 크리에이터 이코노미 최신 트렌드는?
  - #BuldakChallenge 트렌드 분석해줘

질문을 입력하세요 (종료: exit):
> _
```

#### 질문 → 답변 플로우
```
> 최근 1주일 가장 핫한 해시태그는?

🔍 검색 중...                              [애니메이션]
📊 2025-01-08 ~ 2025-01-15 데이터 조회 완료

✨ 답변:
최근 1주일(1/8-1/15) 가장 핫한 해시태그 Top 3:

1. #BuldakChallenge (1,200,000 뷰)
   - 트렌드 점수: 92/100
   - 카테고리: Food & Cooking
   - 주요 사운드: "Fire Alarm Remix"
   - 💡 활용법: 제품 리뷰 + 리액션 조합

2. #SpicyNoodleReview (850,000 뷰)
   - 트렌드 점수: 78/100
   - 💡 활용법: 먹방 + ASMR 스타일

3. #KoreanFoodChallenge (650,000 뷰)
   - 트렌드 점수: 71/100
   - 💡 활용법: 문화 스토리텔링

📈 인사이트:
겨울철(1월) 스파이시 챌린지가 폭발적 성장 중.
식품 카테고리 콘텐츠가 전체 트렌드의 40% 차지.

📎 출처: Airtable 'tiktok_trends' (7 records, 1/8-1/15)

[실행 시간: 8.2초]

> _
```

#### 에러 처리
```
> 내일 날씨는?

❌ 죄송합니다. 현재 데이터에는 해당 정보가 없습니다.

💡 이 에이전트는 틱톡 트렌드와 크리에이터 이코노미 관련 질문만 답변할 수 있습니다.

> _
```

---

## 📊 성과 지표 (KPI)

### 정량적 지표

| 지표 | 목표 | 측정 방법 | 중요도 |
|------|------|-----------|--------|
| **데이터 수집 성공률** | 95% 이상 | Airtable 레코드 수 / 예상 수 | ⭐⭐⭐⭐⭐ |
| **질의응답 정확도** | 80% 이상 | 샘플 20개 정답 수 / 20 | ⭐⭐⭐⭐⭐ |
| **평균 응답 시간** | 10초 이내 | CLI 타이머 측정 | ⭐⭐⭐⭐ |
| **토큰 비용** | 월 $5 이하 | Claude + GPT API 대시보드 | ⭐⭐⭐ |
| **가동률** | 7일 연속 작동 | n8n 실행 로그 확인 | ⭐⭐⭐⭐⭐ |

### 정성적 지표

| 지표 | 평가 기준 | 중요도 |
|------|-----------|--------|
| **사용성** | 비기술자도 CLI 사용 가능한가? | ⭐⭐⭐⭐ |
| **유용성** | 답변이 실무에 활용 가능한 인사이트를 포함하는가? | ⭐⭐⭐⭐⭐ |
| **신뢰성** | 출처가 명확하고, 환각이 없는가? | ⭐⭐⭐⭐⭐ |
| **바이브코딩** | CLAUDE.md 200줄 이내 + 도메인별 문서 분리 | ⭐⭐⭐⭐⭐ |
| **포트폴리오** | 채용 담당자가 "이 사람은 이해했구나" 생각하는가? | ⭐⭐⭐⭐⭐ |

### 비즈니스 임팩트

| 지표 | Before (수동) | After (에이전트) | 개선율 |
|------|---------------|------------------|--------|
| **일일 리서치 시간** | 120분 | 10분 | **92% 단축** |
| **주간 리서치 시간** | 10시간 | 1시간 | **90% 단축** |
| **월간 비용** | $0 (시간 비용) | $7 (API 비용) | - |
| **데이터 누적** | 어려움 | 자동 (Airtable) | - |
| **인사이트 품질** | 주관적 | LLM 기반 객관적 | - |

---

## 🔒 제약 조건 (Constraints)

### 기술적 제약

1. **API 한도**
   - Apify: 월 50,000 results (무료 플랜)
   - Claude API: Pay-as-you-go (예산 월 $3)
   - Airtable: 1,200 rows (무료 플랜)

2. **개발 기간**
   - MVP: 1주일 (Day 1-7)
   - 하루 작업 시간: 4-6시간

3. **기술 스택 고정**
   - n8n (변경 불가 - 채용 요건)
   - Claude + GPT API (변경 불가 - 채용 요건)

### 비즈니스 제약

1. **포트폴리오 목적**
   - 실제 사용자는 본인 1명
   - 프로덕션 레벨 확장성 불필요

2. **비용 제한**
   - 총 예산: 월 $10 이하
   - 무료 티어 최대한 활용

### 법적/윤리적 제약

1. **데이터 수집**
   - 공개 데이터만 수집 (TikTok public API, RSS)
   - 개인정보 수집 금지

2. **AI 윤리**
   - 환각 방지 (데이터 기반 답변만)
   - 출처 명시 (투명성)

---

## 📅 릴리즈 계획

### v1.0 (MVP) - 2025-01-22 (1주일)

**목표**: "작동하는 에이전트" 증명

- [x] 에이전트 1, 2, 3 모두 구현
- [x] CLI 인터페이스
- [x] README + CLAUDE.md
- [x] 샘플 질문 20개 테스트

### v1.1 (고도화) - 2025-01-25 (+3일)

**목표**: Should-have 기능 추가

- [ ] ChromaDB 벡터 검색
- [ ] Slack 통합
- [ ] 주간 리포트

### v2.0 (확장) - 추후

**목표**: Nice-to-have 기능

- [ ] Streamlit Web UI
- [ ] 트렌드 예측 모델
- [ ] API 엔드포인트

---

## 📝 변경 이력 (Change Log)

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v1.0 | 2025-01-15 | 초안 작성 | [Your Name] |

---

## ✅ 승인 (Approval)

| 역할 | 이름 | 날짜 | 서명 |
|------|------|------|------|
| **작성자** | [Your Name] | 2025-01-15 | ✅ |
| **검토자** | (본인) | 2025-01-15 | ✅ |

---

*이 문서는 프로젝트의 "무엇을?" 정의합니다. "왜?"는 Ideation.md, "어떻게?"는 TechStack.md와 Tasks.md를 참조하세요.*
