# Tutorial Content Extraction Guide

## 자동 추출 패턴

세션 대화에서 튜토리얼 콘텐츠를 추출할 때 사용하는 패턴입니다.

### 1. 명령어 추출

대화에서 실행한 모든 bash 명령어를 추출합니다.

**추출 규칙**:
- Bash tool 호출 내역 수집
- 순서대로 정렬
- 중복 제거
- 설명 코멘트 추가

**예시**:
```bash
# 프로젝트 클론
git clone https://github.com/user/repo.git

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 2. 파일 생성/수정 추출

**추출 대상**:
- Write tool로 생성한 파일
- Edit tool로 수정한 파일

**튜토리얼 형식**:
```markdown
### 파일 생성: `path/to/file.js`

다음 내용으로 파일을 생성합니다:

```javascript
[파일 내용]
```

**설명**: [파일의 역할과 중요 포인트]
```

### 3. API 키 설정 추출

대화에서 언급된 모든 API 키/환경 변수를 추출합니다.

**튜토리얼 형식**:
```markdown
### 환경 변수 설정

`.env` 파일을 생성하고 다음을 입력하세요:

```env
AIRTABLE_API_KEY=your_key_here
AIRTABLE_BASE_ID=your_base_id
CLAUDE_API_KEY=your_claude_key
```

**발급 방법**:
- Airtable: [링크] → Settings → API
- Claude: [링크] → API Keys
```

### 4. 문제 해결 추출

대화 중 발생한 오류와 해결 방법을 추출합니다.

**추출 규칙**:
- 오류 메시지
- 원인 분석
- 해결 방법
- 재발 방지 팁

**튜토리얼 형식**:
```markdown
## 자주 발생하는 문제

### 문제 1: "Module not found"
**원인**: 의존성 미설치
**해결**:
```bash
pip install -r requirements.txt
```

### 문제 2: "API rate limit exceeded"
**원인**: API 호출 한도 초과
**해결**:
- 요청 간격을 늘리거나
- 캐싱 구현
```

### 5. 검증 체크리스트 생성

각 단계별 성공 확인 항목을 자동 생성합니다.

**생성 규칙**:
```markdown
**확인 사항**:
- [ ] [명령어 실행 시] 오류 없이 완료
- [ ] [파일 생성 시] 파일이 올바른 경로에 존재
- [ ] [API 테스트 시] 200 응답 코드 수신
- [ ] [워크플로우 실행 시] 모든 노드 초록불
```

## 세션 종료 시 자동 실행

`update-tutorial.sh` 훅이 실행될 때:

1. 세션 대화 분석
2. 위 패턴으로 콘텐츠 추출
3. Tutorial.md에 새 섹션 추가
4. Git 커밋 (선택)

**추가 템플릿**:
```markdown
---

## 📝 [날짜] 세션 업데이트

### 추가된 기능
- [기능 1]
- [기능 2]

### 새로운 단계
[자동 생성된 튜토리얼 내용]

### 알려진 이슈
- [이슈 1]: [해결 방법]
```
