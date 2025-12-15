# Claude Code 설정 및 Skills

이 폴더는 Claude Code 워크플로우 최적화 및 바이브코딩 가이드라인을 포함합니다.

## 폴더 구조

```
.claude/
├── hooks/                          # 자동 실행 스크립트
│   └── update-tutorial.sh          # 세션 종료 시 Tutorial.md 업데이트
├── skills/                         # 도메인별 코딩 가이드
│   ├── agent-dev-guidelines/       # 에이전트 개발 (바이브코딩)
│   │   ├── SKILL.md                # 핵심 원칙 (맥도날드 시스템, 7단계)
│   │   ├── ARCHITECTURE.md         # 아키텍처 패턴
│   │   ├── TOOL_USE.md             # n8n, LLM, Airtable 사용법
│   │   └── WORKFLOWS.md            # n8n 워크플로우 패턴
│   ├── prompt-engineering/         # 프롬프트 엔지니어링
│   │   ├── SKILL.md                # 환각 방지 전략
│   │   ├── FEW_SHOT.md             # Few-shot 예제
│   │   ├── SAMYANG_STYLE.md        # 삼양식품 스타일 가이드
│   │   └── SYSTEM_PROMPTS.md       # Agent 1/2/3 시스템 프롬프트
│   ├── tutorial-generator/         # 튜토리얼 자동 생성
│   │   ├── SKILL.md                # 튜토리얼 구조
│   │   ├── TEMPLATES.md            # 템플릿 모음
│   │   └── EXTRACTION.md           # 세션에서 콘텐츠 추출
│   └── mcp-server-dev/             # MCP 서버 개발
│       ├── SKILL.md                # MCP 개요
│       ├── IMPLEMENTATION.md       # TikTok MCP 서버 구현
│       └── PROTOCOL.md             # MCP 프로토콜 상세
├── settings.json                   # Claude Code 전역 설정
├── skill-rules.json                # Skills 로딩 규칙
└── README.md                       # 이 파일
```

## 주요 기능

### 1. Hooks (자동화)

**session-end hook**:
- 대화 세션 종료 시 자동 실행
- Tutorial.md에 세션 로그 추가
- 타임스탬프 기록

### 2. Skills (코딩 가이드)

Skills는 특정 키워드로 자동 트리거되는 도메인 전문 가이드입니다.

| Skill | 트리거 키워드 | 우선순위 | 자동 로드 |
|-------|--------------|---------|----------|
| **agent-dev-guidelines** | "에이전트 개발", "n8n" | High | ✅ |
| **prompt-engineering** | "프롬프트", "LLM" | High | ✅ |
| **tutorial-generator** | "튜토리얼", "문서화" | Medium | ❌ |
| **mcp-server-dev** | "MCP" | Medium | ❌ |

### 3. 설정 최적화

**Token 최적화**:
- 최대 200,000 토큰 사용
- 150,000 토큰 후 자동 요약
- 중요 문서 보존 (PRD.md, Ideation.md, skills)

**바이브코딩 원칙**:
- CLAUDE.md 200줄 엄수
- 도메인별 문서 분리
- 중요한 것만 Git 커밋

## 사용 방법

### Skills 활성화

Claude Code 세션에서 키워드를 사용하면 자동으로 해당 skill이 로드됩니다:

```
사용자: "n8n 워크플로우를 만들어줘"
→ agent-dev-guidelines skill 자동 로드
→ SKILL.md, ARCHITECTURE.md, WORKFLOWS.md 참조
```

### 수동 Skill 로드

```
사용자: "MCP 서버 개발 가이드를 보여줘"
→ mcp-server-dev skill 로드
```

### Hook 실행 확인

세션 종료 후:
```bash
# Tutorial.md 하단에 자동 추가됨
---
## 📝 Session Log
**Last Updated**: 2025-01-15 14:30:00
```

## 커스터마이징

### 새로운 Skill 추가

1. `.claude/skills/your-skill/` 폴더 생성
2. `SKILL.md` 파일 작성
3. `skill-rules.json`에 등록:

```json
{
  "skills": {
    "your-skill": {
      "description": "설명",
      "trigger": ["키워드1", "키워드2"],
      "priority": "medium",
      "autoLoad": false,
      "files": [".claude/skills/your-skill/SKILL.md"]
    }
  }
}
```

### Hook 수정

`.claude/hooks/update-tutorial.sh` 파일을 편집하여 원하는 자동화를 추가할 수 있습니다.

## 바이브코딩 원칙 적용

이 폴더 구조는 삼양식품 DXT팀의 바이브코딩 방법론을 충실히 따릅니다:

### 1. 맥도날드 시스템
- **본사**: SKILL.md (핵심 가이드)
- **지점장**: skill-rules.json (실행 규칙)
- **알바**: Claude Code (자동 실행)

### 2. 7단계 워크플로우
각 skill은 7단계 워크플로우를 따라 작성되었습니다.

### 3. 3대 원칙
- **빠른 시작**: SKILL.md는 간결하게 (200줄 이내)
- **어펜딕스 참조**: 상세 내용은 별도 파일 (IMPLEMENTATION.md 등)
- **휘발성 컨텍스트**: 중요 파일만 Git 커밋, 임시 실험은 로컬

## 비용 최적화

**토큰 절약 전략**:
- Skills는 필요 시에만 lazy loading
- 세션당 최대 2개 skill 동시 로드
- Skill당 10,000 토큰 제한
- 5,000 토큰 초과 시 자동 요약

**예상 비용**:
- 일반 세션: ~50,000 토큰 ($0.15)
- Skill 활용 세션: ~70,000 토큰 ($0.21)
- 월 예상: $5-10 (하루 2-3 세션 기준)

## 참고 자료

- [삼양식품 바이브코딩 가이드](../삼양식품_바이브코딩_표준화_인사이트.md)
- [TikTok Research Agent PRD](../TikTok-Research-Agent/docs/PRD.md)
- Claude Code 공식 문서

---

*이 설정은 삼양식품 DXT팀 포트폴리오 프로젝트를 위해 최적화되었습니다.*
