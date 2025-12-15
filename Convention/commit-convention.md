# 🧭 Commit Convention

이 저장소는 **Conventional Commits** 기반에,  
AI/에이전트 작업 특성을 고려한 타입을 추가하여 사용합니다.

---

## 1. Commit Message Format
```
<type>(<scope>): <subject>
<body> # optional <footer> # optional 
```
- subject: 명령형, 72자 이내, 마침표 X
- scope: 선택 (예: ai, agent, backend, docs, workflow 등) 

## 2. Types
### 기본 타입
| type     | 설명                  |
| -------- | ------------------- |
| feat     | 새로운 기능 추가           |
| fix      | 버그 수정               |
| docs     | 문서/주석 수정            |
| style    | 코드 스타일 변경(기능 변화 없음) |
| refactor | 구조 개선(기능 변화 없음)     |
| perf     | 성능 개선               |
| test     | 테스트 추가/수정           |
| build    | 빌드/의존성 변경           |
| ci       | CI/CD 설정 변경         |
| chore    | 기타 유지보수             |

### AI/Agent 특화 타입
| type     | 설명                     |
| -------- | ---------------------- |
| agent    | 에이전트 자동 생성 결과/업데이트     |
| workflow | 멀티 모델/에이전트 워크플로우 설계·수정 |
| prompt   | 프롬프트/시스템 지시 변경         |
| dataset  | 데이터·코퍼스·라벨링 자산 추가/수정   |

## 3. Scope (예시)
```
ai, agent, workflow, backend, frontend, infra, docs, rag, vector, prompt, data, test
```
## 4. Examples
```
docs: add AI agent troubleshooting log
agent: upload auto-generated files from Claude Code
workflow(ai): add multi-agent checklist execution
prompt(ai): refine system prompt for task routing
dataset(data): add initial corpus for trend analysis
fix(backend): handle timeout during large context processing
```
### 상세 예시:
```
docs(ai): add troubleshooting log (token optimization)
- documented token limit issues
- introduced Claude/GPT multi-model separation
Refs: #12
```
## 5. BREAKING CHANGE
하위 호환이 깨질 경우 footer에 명시:
BREAKING CHANGE: renamed agent bootstrap script

## 6. Quick Template
``` 
<type>(<scope>): <subject>

- 변경 사항 요약
- 필요 시 설계 의도/배경

Refs: #<id>
BREAKING CHANGE: <내용>
```
## 7. Recommended Tools (Optional)
```
commitlint + husky
conventional-changelog
```