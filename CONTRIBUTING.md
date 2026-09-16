# Skill 을 어디에 둘 것인가

## 3층 구분

```
CLAUDE.md          → 이 프로젝트는 무엇인가. 항상 알아야 하는 정보와 규칙.
Project Skill      → 이 프로젝트에서 이 작업을 어떻게 하는가.  (<project>/.claude/skills/)
Shared Skill       → 일반적으로 이 작업을 어떻게 하는가.        (이 repo)
```

판별 한 줄: **프로젝트 이름을 지웠을 때 의미가 남으면 shared, 사라지면 project.**

## 승격 기준 6문항

프로젝트에서 만든 Skill 을 이 repo 로 옮기기 전에 확인한다.

1. 다른 프로젝트에서도 쓸 수 있는가
2. 특정 프로젝트 이름을 제거해도 의미가 유지되는가
3. 특정 DB schema / API / domain model 에 의존하지 않는가
4. 특정 infrastructure resource 에 의존하지 않는가
5. business rule 이 포함되어 있지 않은가
6. secret / private information 이 포함되어 있지 않은가

**6개 모두 YES 여야 승격한다.** 하나라도 NO 면 프로젝트 안에 남긴다.
하나만 NO 라면 그 부분을 프로젝트에 남기고 나머지 절차만 떼어 승격하는 방법을 먼저 검토한다.

## 예시

| 내용 | 위치 |
|---|---|
| "하루에 녹음을 5회 수행한다" | 프로젝트 CLAUDE.md (domain rule) |
| "Spring API 에서 transaction boundary 를 검토하는 절차" | shared skill |
| "이 repo 는 pnpm 을 쓰고 배포는 Vercel 이다" | 프로젝트 CLAUDE.md |
| "실행계획을 보고 인덱스를 선정하는 기준" | shared skill |
| "주문 취소는 결제 승인 전에만 가능하다" | 프로젝트 CLAUDE.md |

## 새 Skill 추가 규칙

- **축을 확인한다.** 작성 / 검토 / 진단 / 설계 중 어디인가. 기존 Skill 과 같은 축·같은 대상이면
  새로 만들지 말고 기존 것에 합치거나 `references/` 로 넣는다.
- `description` 에는 **트리거 문구**와 **쓰지 않아야 할 경우**(어떤 Skill 로 보낼지)를 같이 적는다.
  이것이 Skill 간 경계를 실제로 강제하는 유일한 수단이다.
- 프로젝트 고유 규칙과 충돌하면 **프로젝트 CLAUDE.md 가 우선**한다는 문장을 SKILL.md 끝에 둔다.
- 커밋 전 확인:

```bash
claude plugin validate ~/git/claude-skills
grep -rniE 'localhost:[0-9]|https?://|apikey|api_key|secret|token|password|arn:aws|\.vercel\.app|firebaseio' skills/
```

두 번째 명령이 무언가를 찾아내면 그것이 정말 일반 예시인지 확인한다.

## 커밋하는 것 / 로컬에만 두는 것

| 커밋 | 로컬 전용 (`.gitignore`) |
|---|---|
| `.claude-plugin/*.json` | `.claude/settings.local.json` |
| `skills/**/SKILL.md`, `references/**` | `.idea/`, `.vscode/`, `.DS_Store` |
| `README.md`, `CONTRIBUTING.md`, `.gitignore` | `.env*` |

`~/.claude/settings.json` 의 `extraKnownMarketplaces` / `enabledPlugins` 항목은 **로컬 머신 설정**이므로
이 repo 에 커밋하지 않는다. 새 머신에서는 README 의 설치 명령 두 줄을 다시 실행한다.
