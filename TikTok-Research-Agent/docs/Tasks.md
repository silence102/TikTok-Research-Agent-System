# 구현 작업 계획 (Tasks)

> 1주일 MVP 완성을 위한 Day-by-Day 작업 계획

---

## 📅 전체 일정 개요

| Day | 주요 작업 | 목표 산출물 | 예상 시간 |
|-----|-----------|-------------|-----------|
| **Day 1-2** | 환경 구축 + 에이전트 1 | n8n 워크플로우 1개 + Airtable 데이터 | 8-12시간 |
| **Day 3-4** | 에이전트 2 | n8n 워크플로우 1개 + 뉴스 요약 | 8-10시간 |
| **Day 5-7** | 에이전트 3 + 문서화 | CLI 프로그램 + README + CLAUDE.md | 12-16시간 |

**총 예상 시간**: 28-38시간 (하루 4-6시간 × 7일)

---

## 📋 Day 1-2: 환경 구축 + 에이전트 1

### 🎯 목표
- n8n 로컬 설치 및 설정 완료
- Airtable Base 생성 및 스키마 설계
- 에이전트 1 (틱톡 트렌드 수집) 완전 작동
- 실제 데이터 10+ rows 수집

---

### ✅ Day 1 체크리스트

#### 1. 프로젝트 초기 설정 (1시간)

```bash
# GitHub 리포지토리 생성
- [ ] GitHub에서 "TikTok-Research-Agent" 리포지토리 생성
- [ ] 로컬 클론: git clone <repo-url>
- [ ] 폴더 구조 생성:
      TikTok-Research-Agent/
      ├── README.md
      ├── CLAUDE.md
      ├── .env.example
      ├── .gitignore
      ├── docs/
      ├── n8n-workflows/
      ├── src/
      ├── scripts/
      └── demo/

# .gitignore 작성
- [ ] .env 추가
- [ ] node_modules/ 추가
- [ ] __pycache__/ 추가
- [ ] data/ 추가
```

#### 2. Airtable 설정 (1시간)

```
- [ ] Airtable 계정 생성 (무료 플랜)
- [ ] Base 생성: "TikTok Research"
- [ ] 테이블 1 생성: "tiktok_trends"
      필드 추가:
      - [ ] date (Date)
      - [ ] hashtag (Single Line Text)
      - [ ] views (Number)
      - [ ] posts_count (Number)
      - [ ] trend_score (Number)
      - [ ] category (Single Select: Food, Dance, Comedy, Beauty, Education, Lifestyle, Challenge, Other)
      - [ ] top_sounds (Long Text)
      - [ ] keywords (Multiple Select)
      - [ ] engagement_rate (Number)
      - [ ] raw_data (Long Text)

- [ ] Personal Access Token 생성
- [ ] Base ID 복사 (URL에서: app......)
- [ ] .env 파일에 저장:
      AIRTABLE_PAT=pat.....
      AIRTABLE_BASE_ID=app.....
```

#### 3. Apify 설정 (30분)

```
- [ ] Apify 계정 생성 (무료 플랜)
- [ ] TikTok Hashtag Scraper Actor 찾기
      URL: https://apify.com/clockworks/tiktok-hashtag-scraper
- [ ] 테스트 실행 (해시태그 "buldak" 1개로 테스트)
- [ ] API Token 생성
- [ ] .env 파일에 저장:
      APIFY_API_TOKEN=apify_api_......
```

#### 4. n8n 로컬 설치 (1시간)

```bash
# Docker로 n8n 설치
- [ ] Docker Desktop 설치 (없는 경우)
- [ ] 터미널에서 실행:
      docker run -it --rm \
        --name n8n \
        -p 5678:5678 \
        -v ~/.n8n:/home/node/.n8n \
        n8nio/n8n

- [ ] 브라우저에서 http://localhost:5678 접속
- [ ] 초기 계정 설정
- [ ] Credentials 추가:
      - [ ] Apify (API Token)
      - [ ] Airtable (Personal Access Token)
      - [ ] OpenAI (API Key - GPT-4o mini)
```

#### 5. docs/DATA_SCHEMA.md 작성 (30분)

```markdown
- [ ] Airtable 스키마 문서화
- [ ] 각 필드의 목적 설명
- [ ] 예시 데이터 추가
```

---

### ✅ Day 2 체크리스트

#### 6. n8n 워크플로우 구축: 에이전트 1 (3-4시간)

**노드 순서**:

```
1. [ ] Schedule Trigger 노드
   - Cron: 0 9 * * * (매일 09:00)
   - Timezone: Asia/Seoul

2. [ ] Set 노드 (해시태그 리스트)
   - 10개 해시태그 배열:
     ["buldak", "foodchallenge", "koreanfood", "spicychallenge",
      "mukbang", "foodreview", "tiktokfood", "viralrecipe",
      "foodtrend", "trending"]

3. [ ] Loop Over Items 노드
   - 각 해시태그마다 반복

4. [ ] HTTP Request 노드 (Apify API)
   - Method: POST
   - URL: https://api.apify.com/v2/acts/clockworks~tiktok-hashtag-scraper/runs
   - Authentication: Header Auth (Bearer Token)
   - Body:
     {
       "hashtags": ["{{$json.hashtag}}"],
       "resultsPerPage": 100,
       "shouldDownloadVideos": false
     }

5. [ ] Wait 노드
   - Time: 2분 (Apify 작업 완료 대기)

6. [ ] HTTP Request 노드 (결과 조회)
   - Method: GET
   - URL: {{$node["HTTP Request"].json.defaultDatasetId}}/items

7. [ ] Function 노드 (데이터 정제)
   - JavaScript 코드 작성:
     * 총 조회수 합계
     * 게시물 수 합계
     * 평균 참여율 계산
     * 트렌드 점수 계산 (0-100)
     * Top 5 사운드 추출
     * 샘플 텍스트 추출 (카테고리 분류용)

8. [ ] OpenAI 노드 (GPT-4o mini)
   - Model: gpt-4o-mini
   - Operation: Message a Model
   - System Prompt: "틱톡 콘텐츠 분류 전문가..."
   - User Message: {{$json.sample_texts}}
   - Temperature: 0.3
   - Response Format: JSON

9. [ ] Function 노드 (최종 데이터 준비)
   - 노드 7과 8 결과 병합
   - Airtable 포맷으로 변환

10. [ ] Airtable 노드 (Create)
    - Base: TikTok Research
    - Table: tiktok_trends
    - Fields Mapping: 모든 필드 연결

11. [ ] IF 노드 (에러 체크)
    - Condition: {{$node["Airtable"].json.id}} exists
    - True: 성공 로깅
    - False: 에러 처리

12. [ ] Set 노드 (성공 로그)
    - 수집 완료 메시지
```

#### 7. 테스트 및 디버깅 (2-3시간)

```
테스트 시나리오:

Test 1: 단일 해시태그 테스트
- [ ] "buldak" 해시태그만으로 수동 실행
- [ ] Apify API 응답 확인
- [ ] Function 노드 출력 확인
- [ ] GPT-4o mini 분류 결과 확인
- [ ] Airtable에 1개 row 생성 확인

Test 2: 전체 워크플로우 테스트
- [ ] 10개 해시태그 전체 실행
- [ ] 각 단계별 로그 확인
- [ ] 에러 발생 시 디버깅
- [ ] Airtable에 10개 rows 확인

Test 3: 데이터 품질 검증
- [ ] 조회수가 숫자인가?
- [ ] 트렌드 점수가 0-100 범위인가?
- [ ] 카테고리가 올바르게 분류되었나?
- [ ] Keywords가 의미 있는가?

에러 패턴 및 해결:
- [ ] Apify timeout → Wait 시간 늘리기
- [ ] GPT API rate limit → Delay 노드 추가
- [ ] Airtable 필드 타입 불일치 → 변환 함수 수정
```

#### 8. n8n 워크플로우 Export (10분)

```
- [ ] n8n UI에서 "Export Workflow" 클릭
- [ ] JSON 파일 다운로드
- [ ] n8n-workflows/agent1-tiktok-trend-collector.json 저장
- [ ] Git commit:
      git add n8n-workflows/agent1-tiktok-trend-collector.json
      git commit -m "feat: Add Agent 1 - TikTok Trend Collector"
```

#### 9. Day 1-2 마무리 (30분)

```
- [ ] Airtable 데이터 확인 (최소 10 rows)
- [ ] 스크린샷 3장:
      1. n8n 워크플로우 전체 화면
      2. Airtable 테이블 뷰
      3. 실행 로그 (성공)
- [ ] demo/screenshots/ 폴더에 저장
- [ ] Git commit 및 push
```

---

## 📋 Day 3-4: 에이전트 2

### 🎯 목표
- Airtable `research_news` 테이블 생성
- RSS 피드 5개 선정 및 테스트
- 에이전트 2 (크리에이터 이코노미 뉴스 수집) 완전 작동
- 요약된 뉴스 5+ rows 수집

---

### ✅ Day 3 체크리스트

#### 10. Airtable 테이블 2 생성 (30분)

```
- [ ] 테이블 생성: "research_news"
      필드 추가:
      - [ ] date (Date)
      - [ ] title (Single Line Text)
      - [ ] source (Single Select: TechCrunch, Medium, Google News, Substack, Reddit)
      - [ ] url (URL)
      - [ ] summary (Long Text)
      - [ ] keywords (Multiple Select)
      - [ ] relevance_score (Number)
      - [ ] sentiment (Single Select: Positive, Neutral, Negative)

- [ ] docs/DATA_SCHEMA.md 업데이트
```

#### 11. Claude API 설정 (30분)

```
- [ ] Anthropic 계정 생성
- [ ] API Key 생성
- [ ] .env 파일에 저장:
      ANTHROPIC_API_KEY=sk-ant-......

- [ ] n8n Credentials 추가:
      - [ ] HTTP Header Auth (Claude API)
```

#### 12. RSS 피드 소스 선정 및 테스트 (1시간)

```
RSS URLs:
- [ ] TechCrunch Creator Economy:
      https://techcrunch.com/tag/creator-economy/feed/

- [ ] Medium Creator Topics:
      https://medium.com/tag/creator-economy/feed

- [ ] Google News:
      https://news.google.com/rss/search?q=creator+economy&hl=en-US&gl=US&ceid=US:en

- [ ] Reddit r/CreatorEconomy:
      https://www.reddit.com/r/CreatorEconomy/.rss

- [ ] Substack (수동 선별):
      (특정 뉴스레터 RSS URL)

각 RSS 테스트:
- [ ] 브라우저에서 XML 확인
- [ ] 최근 24시간 기사 있는지 확인
- [ ] n8n RSS Feed Read 노드로 테스트
```

#### 13. n8n 워크플로우 구축: 에이전트 2 (3-4시간)

**노드 순서**:

```
1. [ ] Schedule Trigger 노드
   - Cron: 0 10 * * * (매일 10:00)

2-6. [ ] RSS Feed Read 노드 × 5개 (병렬)
   - URL: 각각 다른 RSS URL
   - Limit: 20 (최근 20개)

7. [ ] Merge 노드
   - Mode: Combine All
   - 5개 소스 통합

8. [ ] Function 노드 (중복 제거)
   - JavaScript 코드:
     * URL 중복 체크 (Set)
     * 제목 유사도 체크 (Levenshtein distance)
     * 유니크한 기사만 반환

9. [ ] HTTP Request 노드 (전문 가져오기)
   - Loop Over Items
   - URL: {{$json.link}}
   - Readability 또는 직접 파싱

10. [ ] Function 노드 (텍스트 정제)
    - HTML 태그 제거
    - 3,000자 초과 시 자르기 (토큰 절약)

11. [ ] HTTP Request 노드 (Claude API - 관련성 평가)
    - Method: POST
    - URL: https://api.anthropic.com/v1/messages
    - Headers:
      * x-api-key: {{$credentials.ANTHROPIC_API_KEY}}
      * anthropic-version: 2023-06-01
      * content-type: application/json
    - Body:
      {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 256,
        "temperature": 0.5,
        "system": "틱톡 크리에이터 비즈니스 관련성 평가...",
        "messages": [{"role": "user", "content": "..."}]
      }

12. [ ] Filter 노드
    - Condition: {{$json.relevance_score}} >= 70

13. [ ] HTTP Request 노드 (Claude API - 요약)
    - System: "크리에이터 이코노미 리서치 요약 전문가..."
    - Temperature: 0.7
    - Max tokens: 512

14. [ ] Function 노드 (키워드 추출 + 감성 분석)
    - 정규표현식으로 키워드 추출
    - 감성 단어 기반 분류

15. [ ] Airtable 노드 (Create)
    - Table: research_news

16. [ ] Function 노드 (Top 3 선별)
    - relevance_score 순 정렬
    - 상위 3개 선택
```

---

### ✅ Day 4 체크리스트

#### 14. Claude API 프롬프트 최적화 (2-3시간)

**관련성 평가 프롬프트**:
```markdown
- [ ] 프롬프트 작성:
      System: "당신은 틱톡 크리에이터 비즈니스 관련성을 평가하는 전문가입니다.

      평가 기준:
      1. 틱톡 또는 쇼트폼 비디오 플랫폼 언급 (30점)
      2. 크리에이터 수익화, 브랜드 협업 (30점)
      3. 트렌드, 바이럴 마케팅 (20점)
      4. 인플루언서 경제 전반 (20점)

      점수 기준:
      - 90-100: 매우 관련 (틱톡 크리에이터 비즈니스 핵심)
      - 70-89: 관련 (크리에이터 이코노미 일반)
      - 50-69: 부분 관련 (소셜 미디어 일반)
      - 0-49: 관련 없음

      출력 형식 (JSON):
      {
        \"relevance_score\": 85,
        \"reasoning\": \"틱톡 크리에이터 수익화 전략 핵심 내용\",
        \"should_include\": true
      }"

      User: "제목: {{title}}\n출처: {{source}}\n내용: {{content}}"

- [ ] 3개 샘플 기사로 테스트
- [ ] 점수가 합리적인지 검증
```

**요약 프롬프트**:
```markdown
- [ ] 프롬프트 작성:
      System: "크리에이터 이코노미 리서치 요약 전문가입니다.

      요약 원칙:
      1. 한국어로 작성 (원문이 영어여도)
      2. 200자 이내 (핵심만)
      3. 실무 활용 관점 (브랜드 마케터 시각)
      4. 수치, 데이터 포함 시 반드시 명시

      구조:
      - 핵심 메시지 1문장
      - 주요 내용 2-3개 bullet points
      - 실행 인사이트 1문장"

      User: "제목: {{title}}\n출처: {{source}}\n전문: {{content}}"

- [ ] 3개 샘플 기사로 테스트
- [ ] 요약 품질 검증 (간결성, 유용성)
```

#### 15. 테스트 및 디버깅 (2시간)

```
Test 1: RSS 수집
- [ ] 5개 소스 모두 데이터 수집되는가?
- [ ] 중복 제거 정상 작동하는가?

Test 2: Claude API
- [ ] 관련성 평가가 합리적인가?
- [ ] 요약이 200자 이내인가?
- [ ] 한국어로 정확히 번역되었는가?

Test 3: 전체 워크플로우
- [ ] 5개 소스 → 평균 5-10개 기사 저장
- [ ] Airtable에 데이터 정상 저장
- [ ] 실행 시간 15분 이내

에러 해결:
- [ ] RSS 파싱 실패 → 해당 소스 스킵
- [ ] Claude API timeout → Retry 로직 추가
- [ ] 토큰 초과 → 텍스트 자르기 함수 개선
```

#### 16. docs/PROMPTS.md 작성 (1시간)

```markdown
- [ ] 모든 프롬프트 문서화:
      1. 틱톡 카테고리 분류 (GPT-4o mini)
      2. 관련성 평가 (Claude)
      3. 뉴스 요약 (Claude)

- [ ] 각 프롬프트별:
      - 목적
      - System Prompt 전문
      - User Prompt 템플릿
      - 파라미터 (Temperature, Max tokens)
      - 예시 입력/출력
      - 버전 히스토리
```

#### 17. Day 3-4 마무리 (30분)

```
- [ ] n8n 워크플로우 Export:
      n8n-workflows/agent2-research-collector.json

- [ ] Airtable 데이터 확인 (최소 5 rows)

- [ ] 스크린샷 2장:
      1. n8n 워크플로우 (에이전트 2)
      2. Airtable research_news 테이블

- [ ] Git commit 및 push
```

---

## 📋 Day 5-7: 에이전트 3 + 문서화

### 🎯 목표
- Python 프로젝트 초기화
- CLI 인터페이스 구현
- RAG 기반 질의응답 완성
- README.md + CLAUDE.md 작성
- 데모 자료 제작

---

### ✅ Day 5 체크리스트

#### 18. Python 프로젝트 초기화 (1시간)

```bash
# 가상환경 생성
- [ ] cd TikTok-Research-Agent
- [ ] python -m venv venv
- [ ] venv\Scripts\activate (Windows) 또는 source venv/bin/activate (Mac/Linux)

# requirements.txt 작성
- [ ] anthropic==0.18.0
- [ ] openai==1.12.0
- [ ] pyairtable==2.3.0
- [ ] python-dotenv==1.0.0
- [ ] rich==13.7.0 (CLI 꾸미기)

# 설치
- [ ] pip install -r requirements.txt

# 폴더 구조
- [ ] src/agent3/
- [ ] src/data_connectors/
- [ ] src/common/
```

#### 19. Airtable 클라이언트 구현 (2시간)

**파일: src/data_connectors/airtable_client.py**

```python
- [ ] AirtableClient 클래스 작성
      * __init__(api_key, base_id)
      * get_trends(date_filter, limit)
      * get_research(date_filter, limit)
      * search_by_keywords(keywords, table)

- [ ] 날짜 필터 함수:
      * last_7_days()
      * last_30_days()
      * custom_range(start_date, end_date)

- [ ] 테스트:
      python -c "from src.data_connectors.airtable_client import *; test()"
```

#### 20. LLM 클라이언트 구현 (2시간)

**파일: src/common/llm_clients.py**

```python
- [ ] ClaudeClient 클래스:
      * classify_question(question)
      * generate_answer(question, context)

- [ ] 프롬프트 템플릿 (src/agent3/prompts.py):
      * QUESTION_CLASSIFICATION_PROMPT
      * RAG_ANSWER_GENERATION_PROMPT

- [ ] 테스트:
      샘플 질문으로 분류 API 호출 확인
```

---

### ✅ Day 6 체크리스트

#### 21. 질문 처리 엔진 구현 (3-4시간)

**파일: src/agent3/query_engine.py**

```python
- [ ] QueryEngine 클래스:
      * __init__(airtable_client, llm_client)
      * process_question(question)
          1. 질문 분류 (Claude API)
          2. 데이터 조회 (Airtable)
          3. 컨텍스트 준비
          4. 답변 생성 (Claude API)
          5. 후처리 (출처 추가)

- [ ] 헬퍼 함수:
      * prepare_context(records, question_type)
      * extract_keywords(question)
      * format_answer(answer, sources)

- [ ] 심플 RAG (키워드 매칭):
      * keyword_match_score(question, record)
      * select_top_records(records, question, limit=5)
```

#### 22. CLI 인터페이스 구현 (2-3시간)

**파일: src/agent3/cli.py**

```python
- [ ] 시작 화면:
      * ASCII Art 로고
      * 환영 메시지
      * 샘플 질문 3개 표시

- [ ] 메인 루프:
      while True:
          question = input("> ")
          if question == "exit":
              break

          # 로딩 애니메이션
          with spinner("🔍 검색 중..."):
              answer = engine.process_question(question)

          # 답변 출력 (rich 라이브러리로 포맷팅)
          print_answer(answer)

- [ ] 에러 처리:
      * API 에러 → 사용자 친화적 메시지
      * 데이터 없음 → "현재 데이터에는 해당 정보가 없습니다"
```

#### 23. 테스트 (2시간)

```python
# 샘플 질문 5개
Test Questions:
- [ ] "최근 1주일 가장 핫한 해시태그는?"
      * 예상: tiktok_trends 조회 → Top 3 반환

- [ ] "크리에이터 이코노미 최신 트렌드는?"
      * 예상: research_news 조회 → 뉴스 요약 3개

- [ ] "#BuldakChallenge 트렌드 분석해줘"
      * 예상: 특정 해시태그 상세 정보

- [ ] "마이크로 인플루언서 관련 뉴스는?"
      * 예상: 키워드 검색 → 관련 뉴스

- [ ] "내일 날씨는?" (관련 없는 질문)
      * 예상: "현재 데이터에는 해당 정보가 없습니다"

정확도 측정:
- [ ] 5개 중 4개 이상 정확한 답변 (80%+)
- [ ] 평균 응답 시간 10초 이내
```

---

### ✅ Day 7 체크리스트

#### 24. CLAUDE.md 작성 (2시간)

**⭐ 중요: 200줄 이내 엄수**

```markdown
구조 (200줄):
- [ ] 프로젝트 개요 (20줄)
      * 목적, 타겟 유저, 핵심 기능 3가지
      * 기술 스택
      * 리포지토리 구조

- [ ] 코딩 컨벤션 (50줄)
      * Python: Black, snake_case, 타입 힌트
      * n8n: 노드명 규칙, 변수명, 환경변수
      * 프롬프트: 위치, 포맷, 버전 관리

- [ ] 필수 체크사항 (30줄)
      * 보안: API 키 관리
      * 성능: LLM 캐싱, Airtable 배치
      * 에러 처리: try-except, 로깅
      * 테스트: 단위/통합 테스트

- [ ] 자주 하는 작업 (50줄)
      * n8n 워크플로우 수정
      * 새 프롬프트 추가
      * Airtable 스키마 변경
      * 에이전트 3 질문 테스트
      * ChromaDB 재인덱싱

- [ ] 어펜딕스 (50줄)
      * 상세 문서 링크 (docs/)
      * 환경 변수 리스트
      * 데모 시나리오
      * 트러블슈팅

라인 수 체크:
- [ ] wc -l CLAUDE.md 실행
- [ ] 200줄 이내 확인 ✅
```

#### 25. README.md 작성 (2시간)

```markdown
구조:
- [ ] 프로젝트 제목 + 한 줄 설명
- [ ] 데모 영상 또는 GIF (3분)
- [ ] 목차
- [ ] 프로젝트 개요
      * 문제 정의
      * 솔루션 (3개 에이전트)
      * 핵심 기능
- [ ] 기술 스택 (테이블)
- [ ] 빠른 시작
      * 설치
      * 환경 변수 설정
      * Airtable 초기화
      * n8n 워크플로우 임포트
      * 에이전트 3 실행
- [ ] 사용 예시 (코드 블록)
- [ ] 성과 (테이블: 지표 / 목표 / 달성)
- [ ] 문서 링크 (docs/)
- [ ] 배운 점
      * 바이브코딩 원칙 적용
      * n8n 마스터리
      * LLM API 활용
- [ ] 향후 계획 (Should-have, Nice-to-have)
- [ ] 라이선스
- [ ] 작성자 정보
```

#### 26. 데모 자료 제작 (2-3시간)

```
- [ ] demo/sample_questions.md 작성:
      20개 샘플 질문 + 예상 답변

- [ ] 스크린샷 (demo/screenshots/):
      1. [ ] CLI 시작 화면
      2. [ ] 질문 → 답변 예시 (트렌드)
      3. [ ] 질문 → 답변 예시 (리서치)
      4. [ ] n8n 워크플로우 전체 (에이전트 1)
      5. [ ] n8n 워크플로우 전체 (에이전트 2)
      6. [ ] Airtable 테이블 뷰 (tiktok_trends)
      7. [ ] Airtable 테이블 뷰 (research_news)

- [ ] (선택) 데모 영상 촬영:
      * OBS Studio 또는 화면 녹화
      * 3-5분 분량
      * 시나리오:
        1. CLI 실행
        2. 샘플 질문 3개 입력
        3. Airtable 데이터 확인
        4. n8n 워크플로우 보여주기
```

#### 27. 최종 점검 및 Git Push (1시간)

```
체크리스트:
- [ ] 모든 파일 Git add
- [ ] .env는 .gitignore에 있는지 확인
- [ ] CLAUDE.md 200줄 이내 재확인
- [ ] README.md 링크 모두 작동하는지 확인
- [ ] requirements.txt 최신인지 확인

Git 커밋:
- [ ] git add .
- [ ] git commit -m "feat: Complete MVP - 3 Agents + CLI + Docs"
- [ ] git push origin main

GitHub 리포지토리 정리:
- [ ] About 섹션 작성 (짧은 설명 + 태그)
- [ ] Topics 추가: tiktok, ai-agent, n8n, claude, portfolio
- [ ] README.md 렌더링 확인
- [ ] 이미지 링크 정상 확인

최종 확인:
- [ ] 다른 사람 입장에서 README 읽어보기
- [ ] 설치 가이드 따라해보기 (새 환경에서)
- [ ] 샘플 질문 3개 테스트
```

---

## 📊 마일스톤 (Milestones)

### Milestone 1: 환경 구축 완료 (Day 2 종료)
- [x] n8n 로컬 작동
- [x] Airtable 테이블 1 생성
- [x] 에이전트 1 완전 작동
- [x] 실제 데이터 10+ rows

### Milestone 2: 데이터 수집 완료 (Day 4 종료)
- [x] 에이전트 1, 2 모두 작동
- [x] Airtable 양 테이블에 데이터
- [x] 프롬프트 문서화 완료

### Milestone 3: MVP 완성 (Day 7 종료)
- [x] 에이전트 3 CLI 작동
- [x] CLAUDE.md (200줄 이내)
- [x] README.md + 데모 자료
- [x] GitHub 공개

---

## ⚠️ 리스크 관리

### 리스크 1: 시간 부족

**증상**: Day 5 시작했는데 Day 7이 다가옴

**대응**:
1. Should-have 기능 포기 (ChromaDB, Slack)
2. 데모 영상 제작 생략 (스크린샷만)
3. 샘플 질문 20개 → 10개로 축소

### 리스크 2: API 비용 초과

**증상**: Claude API 비용이 예상보다 높음

**대응**:
1. 캐싱 즉시 구현
2. GPT-4o mini로 일부 대체
3. 테스트 횟수 줄이기 (프롬프트 완성도 높이기)

### 리스크 3: 기술적 막힘

**증상**: n8n 또는 Python 코드가 작동 안 됨

**대응**:
1. n8n 커뮤니티 포럼 검색
2. Claude Code에게 디버깅 요청
3. 최소한으로 작동하는 버전부터 (MVP의 MVP)

---

## ✅ 최종 체크리스트

### 코드
- [ ] 에이전트 1 n8n 워크플로우 작동
- [ ] 에이전트 2 n8n 워크플로우 작동
- [ ] 에이전트 3 CLI 작동
- [ ] 모든 프롬프트 문서화 (docs/PROMPTS.md)

### 문서
- [ ] README.md (프로젝트 개요, 설치, 사용법)
- [ ] CLAUDE.md (200줄 이내!)
- [ ] docs/PRD.md (완성)
- [ ] docs/ARCHITECTURE.md (시스템 구조)
- [ ] docs/DATA_SCHEMA.md (Airtable 스키마)

### 데모
- [ ] demo/sample_questions.md (10개 이상)
- [ ] demo/screenshots/ (5장 이상)
- [ ] (선택) demo/demo_video.mp4

### 테스트
- [ ] 에이전트 1 수동 실행 3회 이상
- [ ] 에이전트 2 수동 실행 3회 이상
- [ ] 에이전트 3 샘플 질문 5개 이상
- [ ] 정확도 80% 이상 달성

### Git
- [ ] .gitignore 설정 (.env 포함)
- [ ] 모든 파일 커밋
- [ ] GitHub 리포지토리 공개
- [ ] README.md 렌더링 확인

---

**🎯 1주일 후 목표: "작동하는 에이전트"를 증명하는 완전한 포트폴리오!**
