# 에이전트 아키텍처 패턴

## 모듈화 설계

### 독립 에이전트 원칙
각 에이전트는 독립적으로 작동하며, 하나가 실패해도 나머지는 정상 작동합니다.

```
[Agent 1] 데이터 수집 → [Storage]
[Agent 2] 데이터 가공 → [Storage]
[Agent 3] 데이터 활용 → [Output]
```

## 데이터 중심 설계

- **중앙 데이터베이스**: Airtable 활용 (GUI 접근 가능)
- **구조화된 데이터**: 환각 방지를 위한 스키마 정의
- **출처 추적**: 모든 데이터에 source 필드 포함

## n8n 워크플로우 패턴

### 기본 구조
1. **Trigger Node**: Schedule/Webhook
2. **Data Collection**: HTTP Request/API Call
3. **Processing**: Code/Function Node
4. **LLM Integration**: Claude/GPT API
5. **Storage**: Airtable/Database
6. **Notification**: Slack/Email (선택)

### 에러 핸들링
- Try-Catch 노드로 예외 처리
- 실패 시 Slack 알림
- 재시도 로직 구현
