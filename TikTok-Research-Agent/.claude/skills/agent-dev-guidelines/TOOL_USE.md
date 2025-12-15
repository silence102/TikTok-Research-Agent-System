# 도구 활용 가이드

## n8n 핵심 노드

### 필수 노드
- **Schedule Trigger**: 크론 스케줄링 (매일 09:00 등)
- **HTTP Request**: API 호출
- **Code**: JavaScript/Python 커스텀 로직
- **Set**: 데이터 변환
- **IF**: 조건 분기
- **Merge**: 데이터 병합

### 통합 노드
- **Claude/OpenAI**: LLM API
- **Airtable**: 데이터베이스
- **Slack**: 알림
- **RSS Feed**: 뉴스 수집

## LLM API 최적화

### Claude vs GPT 선택 기준
- **Claude 3.5 Sonnet**: 고품질 요약/답변 (한국어 우수)
- **GPT-4o mini**: 간단한 파싱/분류 (비용 1/20)

### 토큰 절약 전략
- 시스템 프롬프트 캐싱
- 배치 처리
- Temperature 0.3 (일관성 확보)

## Airtable 스키마 설계

### 기본 필드
- `id`: Primary Key (자동 생성)
- `created_at`: 수집 시간
- `source`: 출처 URL
- `raw_data`: 원본 데이터 (JSON)
- `summary`: LLM 요약 결과
- `category`: 분류 태그
