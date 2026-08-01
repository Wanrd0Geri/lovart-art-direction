---
name: lovart-art-direction
description: 将用户的一句中文设计诉求、参考图和续做包，编译为一份可直接粘贴给 Lovart Agent 的中文总提示词，并默认指定 Nano Banana Pro。用于原创角色、场景、特效、怪物、道具、世界观、多方向调研、门派或地域系列、批量编号生成和跨新会话续做；强制路由、参考图职责、动态校验批、内部追踪合同、字段隔离和交付前检查。触发示例包括“调研风格”“批量生成”“设计一套”“每种N张”“门派角色”“世界观设定”“题材池”“续做包”“接着上次那批”。不用于单张源图忠实重建、由当前宿主直接生成图片或最终视频提示词。
---

# Lovart Art Direction

Deliver one complete Chinese prompt that the user can paste into Lovart Agent.
Do not generate or edit images, operate Lovart, or claim that research or generation already happened.
Treat this skill as a compiler: route first, compile second, validate third, then deliver.

## Mandatory compilation state machine

Follow every phase in order. Do not draft the final artifact before phases 1-3 pass.

### Phase 1: extract authoritative facts

Extract only facts supplied by the user or restored from an authorized continuity pack:

- asset types and intended use;
- exact deliverable count and any user-defined groups;
- visual direction, motifs, world rules, aspect ratio, resolution, and model request;
- reference images and the attributes each image is authorized to control;
- research owner, planning owner, metadata visibility, pause behavior, and continuation state.

Apply precedence in this order:

1. current explicit user instruction;
2. current image explicitly assigned by the user;
3. self-contained continuity-pack field;
4. route default;
5. asset or quality profile default.

Never convert an incidental image, a previous chat image, or casual recollection into a reference role without authorization.

### Phase 2: create the route manifest

Read [routing-schema.md](references/routing-schema.md) and create one complete route manifest before writing prose.
Choose exactly one value for every required enum.

Hard gate:

- Ask one concise consolidated question when an unresolved answer would materially change identity, reference ownership, deliverable count, grouping ownership, research ownership, or project direction.
- When the user assigns planning to Lovart, set `planning_owner=agent-planned`, `grouping_owner=lovart`, and normally `metadata_mode=internal`; do not ask the host to invent groups.
- Set `continuity_pack=true` with `continuity_reason=program-default` for a program unless the user explicitly declines continuity output.
- Make a reversible assumption only for a non-critical field and record it in `assumptions`.
- If a critical field remains unresolved, stop. Do not compile a provisional prompt.

On Windows, run `powershell -ExecutionPolicy Bypass -File scripts/validate_artifact.ps1 -Route <route.json> -RouteOnly`; the wrapper locates the Codex bundled Python and enables UTF-8. Do not guess with bare `python` or `py -3` first.
On other systems, run `python3 scripts/validate_route.py <route.json>`.
If local execution is genuinely unavailable, apply every schema rule manually and do not claim script validation.

### Phase 3: load exactly one route compiler

Choose exactly one route:

- `explore`: read [explore-compiler.md](references/explore-compiler.md).
- `build`: read [program-compiler.md](references/program-compiler.md). It covers simple, controlled, and program builds.
- `extend`: read [extend-compiler.md](references/extend-compiler.md).

Then read only the relevant profiles:

- Read [asset-profiles.md](references/asset-profiles.md) for every requested asset family.
- Read [quality-profiles.md](references/quality-profiles.md) for the intended medium and use.
- Read [reference-and-continuity.md](references/reference-and-continuity.md) only when references, identity locks, `controlled`, `program`, `extend`, or a continuity pack is involved.

Do not load a second route compiler. Do not follow a second-level reference chain.

### Phase 4: compile typed layers

Read [field-ownership.md](references/field-ownership.md) and compile these layers without field leakage:

1. Lovart interface recommendations;
2. Agent execution contract;
3. shared visual capsule;
4. current item delta or variation constitution;
5. backend rejection checks;
6. continuity pack when required.

Only the shared visual capsule plus the current item delta may reach the image model.
Keep model, aspect ratio, resolution, numbering, research prose, names, reporting, retry logic, and rejection checks out of the image-model input.

### Phase 5: deterministic lint

Save the compiled artifact. On Windows run:

`powershell -ExecutionPolicy Bypass -File scripts/validate_artifact.ps1 -Route <route.json> -Prompt <prompt.txt>`

On other systems run:

`python3 scripts/validate_route.py <route.json>`

`python3 scripts/lint_prompt.py --route <route.json> --prompt <prompt.txt>`

Treat every reported error as blocking. Revise the artifact and rerun until it passes.
Warnings require explicit review but do not automatically block delivery.
If the script is unavailable, perform the same checks manually and state only that manual validation was performed.

### Phase 6: semantic audit

Re-read the original user request, route manifest, and compiled artifact from scratch.
Check:

- every explicit constraint is preserved;
- no unconfirmed grouping, name, reference role, motif, or project direction was invented;
- planning ownership and metadata visibility are respected;
- every requested image remains one independent deliverable unless a design sheet was explicitly requested;
- the visual capsule leads with medium and visible rendering behavior, then culture, subject, and mood;
- the continuity pack records current facts rather than future or unresolved state;
- no fabricated research, interface capability, source, or completion claim appears.

Deliver only after both lint and semantic audit pass.

## Research and named directions

Use exactly one research mode from the route manifest:

- `research-by-host`: verify real cases through available sources and embed only compact executable findings and direct links.
- `research-by-lovart`: instruct Lovart to research, cite sources, mark uncertainty, and separate confirmed facts from synthesis.
- `no-research`: use when the direction and assets are already sufficiently defined.

Treat living creators, studios, genre labels, and work titles as routing clues, not operative image-model style tokens.
Translate them into medium, shape, construction, material response, color, light, density, function, and narrative behavior.
Do not claim attribution or production methods without verification.

## Reference capability gate

Apply the dated API snapshot and the currently verified Lovart surface limit separately.
Use the smaller applicable limit and never present an API allowance as a verified Lovart UI allowance.
See [reference-and-continuity.md](references/reference-and-continuity.md).

## Output surface

Return one reusable Chinese artifact in the user's requested surface. Otherwise use the build surface below. The selected route compiler may replace the middle markers with its route-specific contract:

```text
Lovart Agent 提示词

【Lovart 界面建议】
模型：Nano Banana Pro
建议画幅：任务适配的单一建议
建议分辨率：任务适配的单一建议

【提示词】
【Agent执行合同】
...
【共享视觉胶囊】
...
【变化宪法】或【当前单项差异】
...
【后台拒绝检查】
...

【续做包｜下次继续时完整贴回】
...
```

Replace every placeholder before delivery.
Omit the continuity section only when the route says `continuity_pack=false`.
Do not append an English duplicate, alternatives, or post-artifact explanation.

## Skill modification gate

When modifying this skill, read [regression-cases.md](references/regression-cases.md), run the official `quick_validate.py`, run `powershell -ExecutionPolicy Bypass -File scripts/validate_artifact.ps1 -Regressions` on Windows or `python3 scripts/run_regressions.py` elsewhere, and forward-test representative routes with clean context.
Do not install or publish a revision until all blocking checks pass.
