# n8n 워크플로우 구현 패턴

## Agent 1: 데이터 수집 워크플로우

```
Schedule Trigger (매일 09:00)
  ↓
HTTP Request (Apify API 호출)
  ↓
Code (데이터 파싱)
  ↓
Set (필드 매핑)
  ↓
IF (데이터 유효성 검증)
  ↓ (True)
Airtable Create (저장)
  ↓
Slack (성공 알림)
```

## Agent 2: LLM 처리 워크플로우

```
Schedule Trigger (매일 10:00)
  ↓
RSS Feed Reader (뉴스 수집)
  ↓
Code (중복 제거, 필터링)
  ↓
Claude API (관련성 평가 + 요약)
  ↓
Set (결과 정리)
  ↓
Airtable Create (저장)
```

## Agent 3: 질의응답 워크플로우

```
Webhook Trigger (사용자 질문 수신)
  ↓
Airtable Search (관련 데이터 검색)
  ↓
Code (컨텍스트 구성)
  ↓
Claude API (RAG 기반 답변 생성)
  ↓
HTTP Response (답변 반환)
```

## 에러 핸들링 패턴

```
Try Node
  ↓ (실패 시)
Catch Node
  ↓
Set (에러 정보 기록)
  ↓
Slack (에러 알림)
  ↓
Stop and Error (워크플로우 중단)
```
