# Tutorial Templates

## Template 1: n8n 워크플로우 튜토리얼

```markdown
# [워크플로우 이름] 구축하기

## 목표
이 튜토리얼을 완료하면:
✅ n8n에서 [기능] 워크플로우를 구축할 수 있습니다
✅ [API/서비스]와 통합할 수 있습니다
✅ 크론 스케줄링으로 자동 실행할 수 있습니다

소요 시간: 30-45분
난이도: 초급

## 준비물
- [ ] n8n 설치 완료 (Docker 또는 npm)
- [ ] [API 키/계정]
- [ ] [데이터베이스 접근 권한]

## Step 1: 워크플로우 생성 (5분)
1. n8n 접속 (http://localhost:5678)
2. "+ New Workflow" 클릭
3. 워크플로우 이름 설정: "[이름]"

## Step 2: 트리거 노드 추가 (10분)
1. Schedule Trigger 노드 추가
2. 설정:
   - Mode: Every day
   - Hour: 09
   - Minute: 00

**확인**:
- [ ] Test 버튼 클릭 시 성공 메시지
- [ ] 다음 실행 시간 표시됨

## Step 3: [데이터 수집] 노드 추가 (15분)
...

## Step 4: 테스트 및 배포 (10분)
...

## 문제 해결
| 문제 | 해결 |
|------|------|
| "Connection failed" | API 키 재확인 |
| 노드 실행 안 됨 | 이전 노드 연결 확인 |
```

## Template 2: 에이전트 사용 튜토리얼

```markdown
# [에이전트 이름] 사용 가이드

## 빠른 시작
```bash
# 1. 프로젝트 클론
git clone [URL]

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 4. 실행
python main.py "질문 입력"
```

## 상세 가이드

### 1. 환경 설정 (20분)
...

### 2. 첫 질문하기 (5분)
...

### 3. 고급 기능 (선택)
...

## 예제 시나리오

### 시나리오 1: [유즈케이스]
**목표**: [달성할 것]

**질문 예시**:
```
"최근 일주일 틱톡 트렌드는?"
```

**예상 답변**:
```
[샘플 답변]
```

**활용 방법**:
- [실무 적용 예시]
```

## Template 3: API 통합 튜토리얼

```markdown
# [API 이름] 통합 가이드

## API 키 발급 (10분)
1. [사이트] 접속
2. 회원가입/로그인
3. Settings → API Keys
4. "Generate New Key" 클릭
5. 키 복사 (한 번만 표시됨!)

## 테스트 요청 (5분)
```bash
curl -X POST "https://api.example.com/v1/endpoint" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

**예상 응답**:
```json
{
  "status": "success",
  "data": {...}
}
```

## n8n에서 사용하기 (15분)
...
```
