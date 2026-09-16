# claude-skills

여러 개인 프로젝트에서 재사용하는 Claude Code Skills.
**개발 방법론과 작업 절차만** 담는다. 특정 프로젝트의 도메인 지식·스키마·인프라 정보는 넣지 않는다.

## 구조

```
claude-skills/
├── .claude-plugin/
│   ├── plugin.json         # plugin 매니페스트
│   └── marketplace.json    # 이 repo 자체를 marketplace 로 노출 (source: "./")
└── skills/
    ├── java-spring-backend/SKILL.md
    ├── code-review/SKILL.md + references/spring.md
    ├── database-analysis/SKILL.md
    ├── debugging/SKILL.md
    └── api-design/SKILL.md
```

## 설치 (Claude Code 2.1.x)

```bash
claude plugin marketplace add ~/git/claude-skills
claude plugin install claude-skills@way-skills --scope user
```

user scope 이므로 **모든 프로젝트에서 자동으로 로드된다.** 프로젝트마다 설정할 필요가 없고
복사·submodule·symlink 도 필요 없다.

원격에 올린 뒤에는 경로 대신 GitHub repo 를 넘길 수 있다:

```bash
claude plugin marketplace add wayjeong/claude-skills
```

갱신·확인:

```bash
claude plugin marketplace update way-skills
claude plugin details claude-skills
```

> `permissions.additionalDirectories` 와 `--add-dir` 는 **도구 접근 허용 디렉터리**일 뿐
> Skill 로딩 경로가 아니다. 공통 Skill 공유에 사용하지 않는다.

## Skill 을 고친 뒤

설치된 plugin 은 `~/.claude/plugins/cache/way-skills/claude-skills/<version>/` 에 **복사본**으로
고정된다(설치 시점의 commit sha 로 pin). repo 를 고쳐도 자동 반영되지 않는다.

1. `skills/**` 수정
2. `.claude-plugin/plugin.json` 의 `version` 을 올린다
3. 커밋
4. 반영:

```bash
claude plugin marketplace update way-skills
claude plugin update claude-skills
```

5. Claude Code 세션을 재시작한다 (plugin 변경은 다음 세션부터 적용된다)

검증: `claude plugin details claude-skills` 의 Skills 목록과 버전 확인.

## Skill 역할 경계

| Skill | 언제 |
|---|---|
| `java-spring-backend` | 코드를 **쓸 때** — 계층 배치, 트랜잭션 경계, DTO 경계 |
| `code-review` | 코드를 **볼 때** — diff/PR 검토 절차와 위험도 판정 |
| `database-analysis` | 스키마·쿼리·인덱스·마이그레이션 |
| `debugging` | 이미 **터진 것**의 원인 추적 |
| `api-design` | HTTP 계약 설계와 호환성 판단 |

축이 겹치지 않도록 **작성 / 검토 / 진단 / 설계**로 나눈다.
언어·프레임워크별 항목은 별도 Skill 로 쪼개지 않고 `references/` 로 내린다.

AWS 아키텍처 리뷰는 이 repo 에 두지 않는다. `aws-dev-toolkit` plugin 이
`aws-architect`, `well-architected`, `security-review`, `cost-check` 를 이미 제공한다.

## 여기에 넣지 않는 것

- 프로젝트 business/domain rule, 프로젝트 이름에 종속된 지시
- DB schema, API endpoint 목록, 환경변수, 배포 정보
- 특정 repo 디렉터리 구조에 강하게 의존하는 지시
- AWS/Firebase/Vercel resource ID, URL, credentials, API key/token/secret
- 사용자 데이터·개인정보
- **회사 내부 정보 일체** (아래)

## 회사 프로젝트

이 repo 는 **개인용**이다. 회사 코드·아키텍처·스키마·내부 URL·시스템 이름·고객 정보를
어떤 형태로도 추가하지 않는다. 회사에서 공통 Skill 이 필요하면 회사 환경에서 허용되는
**별도 repository** 를 쓴다. 회사 정책상 외부/개인 repo 연결이 허용되지 않으면
회사 프로젝트와 이 repo 사이에 어떤 참조도 만들지 않는다 (marketplace 등록도 하지 않는다).

## 승격 / 배치 판단

`CONTRIBUTING.md` 참고.
