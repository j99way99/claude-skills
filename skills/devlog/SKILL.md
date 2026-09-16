---
name: devlog
description: >
  방금 한 작업에서 남길 만한 것을 골라 블로그 글 초안으로 만들고, 확인을 받은 뒤
  waysblog 저장소에 브랜치로 push 한다. 어느 저장소에서 작업하든 쓸 수 있다.
  "이거 글로 남겨줘", "devlog 써줘", "이번 작업 블로그에 정리해줘", "지금까지 한 거 회고 글로"
  같은 요청에 트리거된다. 인자로 주제를 좁힐 수 있다 (예: `/devlog 트랜잭션 경계`).
  코드 자체를 문서화하는 것(README, 주석, 저장소 문서)은 여기에 해당하지 않는다.
---

# Devlog → waysblog

한 번 호출 = 한 편. 확인 게이트 하나를 사이에 둔 2단계다.
인자가 있으면 그 주제로 좁히고, 없으면 **가장 최근 글 이후의 작업**을 다룬다.

## 상수

- 블로그 저장소: `https://github.com/j99way99/waysblog.git`
- 작업 경로: `~/git/waysblog`. 있으면 재사용한다 —
  `git -C ~/git/waysblog checkout -q main && git -C ~/git/waysblog pull -q`.
  없을 때만 `--depth 20` 으로 clone 한다.
- 글 파일: `_posts/YYYY-MM-DD-slug.md` (slug 은 kebab-case)
- Frontmatter: `title`(작은따옴표), `date`, `permalink: /posts/YYYY/MM/slug/`, `tags` 목록.
  `claude` 태그는 항상 넣는다.
- 언어: 영어 (사이트 locale 이 `en-US`). 한국어는 요청받았을 때만.

## Phase 1 — 초안 (여기서 절대 push 하지 않는다)

1. **범위 확정.** `ls ~/git/waysblog/_posts | tail -3` 와
   `git -C ~/git/waysblog ls-remote --heads origin 'post-*'` 를 본다.
   merge 되지 않은 `post-*` 브랜치도 **이미 쓴 것으로 친다.**
   가장 최근 글의 날짜 이후 작업을 다루고, 그 제목들이 이미 덮은 주제는 건너뛴다.

2. **작업 내용을 모은다.** 아래 순서로, 글을 쓸 수 있게 된 시점에서 멈춘다.
   **코드베이스를 탐색하지 않는다** — 이미 요약된 것을 쓴다.
   - 이번 세션에서 실제로 한 작업 (대화에 이미 있다)
   - 그 저장소에 작업 로그가 있으면 최신 항목 (예: `logs/LOOPLOG.md` 의 `## Loop notes`)
   - `git log --oneline -10`
   - 위로 부족할 때만 해당 범위의 `git diff --stat`

   로그 파일은 **있는 저장소에만 있다.** 없으면 그냥 git 히스토리와 세션 내용으로 쓴다.

3. **초안을 작업 경로에 쓴다.** 구성:
   문제 → 설계를 결정지은 제약이나 통찰 → 실제로 만든 것 → 실패했거나 실패할 뻔한 것 → 다음 것.
   코드는 **생각을 전달하는 자리에만** 넣는다 (한 덩어리 5~15줄).

4. **문체**는 `_posts/2026-07-29-hello-world.md` 에 맞춘다.
   소문자 문장형 제목, 1인칭, 마케팅 톤 없음, 이모지 없음.

5. **정직성 규칙 — 다듬기보다 이게 우선이다.**
   - 검증한 것과 안 한 것을 구분해서 쓴다. 테스트하지 않은 코드가 동작하는 것처럼 쓰지 않는다.
   - 단계·범위의 한계를 명시한다 (예: "현금 결제만, 카드는 아직").
   - 세션 중에 했던 주장이 틀렸거나 과했으면, 그대로 옮기지 말고 글에서 바로잡는다.
   - 규제나 빠르게 바뀌는 주제에는 단서를 한 줄 단다.

6. 초안 전문을 대화에 출력하고 OK 또는 수정 요청을 묻는다. **여기서 멈춘다.**

## Phase 2 — 발행 (명시적 OK 이후에만)

1. `cd ~/git/waysblog && bundle exec jekyll build` — YAML/렌더 오류를 고치고
   `_site/posts/` 에 글이 생겼는지 확인한다.
2. `post-<slug>` 브랜치, `_posts/*.md` **한 파일만** 스테이징, 커밋,
   `-u` 로 push. 커밋 메시지 끝에 `Co-Authored-By: Claude <noreply@anthropic.com>`.
3. git 이 출력한 PR 링크를 보고한다. **merge 하지 않고 `main` 에 push 하지 않는다.**

## 토큰 절약

- 이미 context 에 있는 파일을 다시 읽지 않는다.
- 수정 요청을 받으면 바뀐 줄만 보여준다. 글 전체를 다시 출력하지 않는다.
- Jekyll 빌드는 Phase 2 에서 한 번만 돌린다.
- 단계 사이에 진행 상황을 서술하지 않는다. 독립적인 명령은 한 번에 묶어서 실행한다.
