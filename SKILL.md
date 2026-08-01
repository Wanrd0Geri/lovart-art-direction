---
name: lovart-art-direction
description: 将用户的一句中文设计诉求、参考图和续做包，编译为一份可直接粘贴给 Lovart Agent 的中文总提示词，并默认指定 Nano Banana Pro。用于原创角色、场景、特效、怪物、道具、世界观、多风格调研、门派或地域系列、批量编号生成和跨新会话续做；自动选择调研责任方、资产质量规则、画幅、分辨率、参考图职责、动态校验批和变化矩阵。触发示例包括“调研风格”“批量生成”“设计一套”“每种N张”“门派角色”“世界观设定”“特效阶段表”“题材池”“续做包”“接着上次那批”。不用于单张源图忠实重建、直接写给图像模型的提示词、由当前宿主直接生成图片或最终视频提示词。
---

# Lovart Art Direction

Deliver one complete Chinese prompt that the user can paste into Lovart Agent.
Do not generate or edit images, operate Lovart, or claim that research or generation already happened.
Never fabricate sources, current interface capabilities, or completed outputs.

## Load only the required references

- Read [output-templates.md](references/output-templates.md) after routing the deliverable, research owner, and complexity.
- Read [asset-profiles.md](references/asset-profiles.md) for every relevant asset type.
- Read [quality-profiles.md](references/quality-profiles.md) after identifying the intended use and medium.
- Read [research-and-variation.md](references/research-and-variation.md) for `program`, research, exploration, multiple directions, variation matrices, or deduplication.
- Read [batch-contract.md](references/batch-contract.md) for `program`, six or more deliverables, grouping, batching, or continuous numbering.
- Read [reference-and-continuity.md](references/reference-and-continuity.md) for `controlled`, `program`, `extend`, references, identity locks, consistency, or a continuity pack.
- Read [prompt-architecture.md](references/prompt-architecture.md) for `controlled`, `program`, negative constraints, named genre labels, concise or high-level prompts, and every task where Lovart will plan or generate images.
- Do not follow a second-level reference chain. Return here after reading the required files.

## Compile the prompt

### 1. Preserve the request

Extract the asset types, intended use, quantity, group counts, visual direction, world rules, required motifs, references, requested research owner, aspect ratio, resolution, and continuation state.
Treat explicit user constraints as authoritative.
Apply them before route defaults. An explicit request for no continuity pack, no pause, internal-only numbering, no names, default resolution, fenced Markdown, or agent-owned planning overrides any later template default that conflicts with it.
Keep requested motifs such as pagodas, waterfalls, white robes, or floating mountains; make them original through structure, function, material, geography, and culture rather than replacing them.
Ask one concise question only when different answers would materially change identity, reference ownership, delivery count, or project direction.
Make a reasonable reversible assumption otherwise and state it inside the Lovart prompt when execution depends on it.

### 2. Route the deliverable

Choose exactly one route:

| Route | Use when | Compile |
| --- | --- | --- |
| `explore` | The direction is unresolved or the user requests research, comparison, or a visual system | Research plan or verified findings, style cards, candidates, verification gate, and release rules |
| `build` | The direction is sufficiently defined | Design rules, numbered deliverables when needed, generation instructions, and quality checks |
| `extend` | The user continues an earlier batch | Restored locks, continuous numbering, new deltas, generation rules, and an updated continuity pack |

Treat every conversation as potentially new.
For `extend`, require either previous approved images or a pasted continuity pack.
Do not reconstruct high-cost identity or style locks from casual recollection alone.

### 3. Route research ownership

Choose exactly one mode:

| Mode | Use when | Action |
| --- | --- | --- |
| `research-by-host` | The user needs real market cases or verifiable attribution and the current host has a usable access route | Search and verify first; embed compact findings and source links in the Lovart prompt |
| `research-by-lovart` | The user explicitly asks Lovart Agent to research, or no host access route exists | Instruct Lovart to research, cite sources, mark uncertainty, and avoid invented cases |
| `no-research` | The direction, assets, and references are already defined | Omit research and move directly to design and generation |

Honor an explicitly assigned research owner.
Choose what happens after research: `research-then-review` waits for approval; `research-then-execute` emits the requested compact findings and continues without waiting. Use the latter when the user requests an uninterrupted run.
When the request only says “调研市面案例”, prefer real host research when available.
Judge access by capability rather than product name: use search or connectors first, browser control for JavaScript, redirects, cookies, or login state, and plain server fetch only as a fallback.
Do not interpret a blocked fetch as evidence that a page or source does not exist.
If every route fails, disclose the failure and switch to `research-by-lovart`; use unsourced synthesis only with user consent.
Convert research into visible design attributes instead of listing titles or artist names as style tokens.

### 4. Route complexity

Judge complexity from quantity, asset diversity, direction count, reference roles, identity locks, research, and cross-session continuity.

| Level | Typical condition | Required structure |
| --- | --- | --- |
| `simple` | One straightforward asset, one to five outputs, no complex reference relations | Goal, necessary reference roles, matching quality profile, generation instruction |
| `controlled` | One asset family, a design sheet, multiple references, identity lock, or other high-cost constraint | Design rules, variation where useful, continuity pack, and numbering for multiple deliverables |
| `program` | Multiple styles, factions, regions, asset types, a large batch, or a worldbuilding program | Full visual system, grouped matrix, numbered contract, verification gate, batch checks, continuity pack |

Do not classify by count alone.
A single multi-reference character sheet may be `controlled`; five mixed worldbuilding assets may be `program`.

### 5. Route assets, format, and quality

Select the primary and secondary asset profiles.
Keep only dimensions relevant to the requested assets.
Choose format by use: favor landscape for environments and integrated VFX, portrait for single characters or creatures, and landscape design sheets for turnarounds or staged VFX.
Honor the user's explicit aspect ratio when currently supported.
Otherwise recommend the nearest supported ratio and add a second crop, outpaint, or layout step only when the current Lovart surface supports it.
Select the matching quality profile instead of applying cinematic realism to every asset.
Translate “高级”, “电影感”, or “有质感” into visible optical, material, structural, painterly, or VFX behavior.
Set the visual hierarchy in this order: medium and rendering behavior, cultural and genre system, subject design, then mood. Treat labels such as `国漫`, `仙侠`, `暗黑神话`, or a work title as research and cultural-routing clues, not as the operative rendering style. When premium CG is requested, lead the visual capsule with visible high-end CG behavior; use engine names only as supporting shorthand.

### 6. Assign every reference a role

Map each reference to only the attributes the user authorizes, such as identity, pose, composition, environment, material, or a named style axis.
Keep all unassigned attributes neutral.
Do not average conflicting references or copy interfaces, arrows, watermarks, or irrelevant text.
Propose the most likely mapping first; ask one consolidated question only when alternate mappings materially change the result.
Apply the dated model/API snapshot and the current Lovart surface limit separately; use the smaller applicable limit.
Never present an API allowance as a verified Lovart interface allowance.

### 7. Build controlled variation

For `program`, six or more outputs, or multiple directions, define fixed attributes, planned variation axes, and forbidden drift.
Choose three or four reasonably independent axes.
Do not let weather, time of day, or palette alone carry the difference between styles.
Choose planning ownership: `host-specified`, `agent-planned`, or `hybrid`. Create a complete tracking contract before generation, but keep it internal to Lovart when the user requests only a high-level constitution or does not want names and per-item details.
Make each number one independent deliverable unless the user explicitly requests a multi-view or multi-stage design sheet.

### 8. Put the verification gate inside Lovart

Deliver the complete prompt in this conversation; never stop after compiling only a small sample.
For `program` and multi-deliverable `controlled` tasks, apply the dynamic verification rules in `batch-contract.md`.
Instruct Lovart to establish the full list and shared rules, generate the verification items, pause inside the Lovart conversation when remaining items exist, update shared rules after feedback, then continue the remaining numbers.
When the user says “不要暂停，直接全部生成”, remove the wait but retain numbering and per-batch quality checks.
Never create an empty “confirm before continuing” pause when the verification set already contains every requested output.

### 9. Compile a layered prompt

Separate the final artifact into an Agent execution contract, a compact shared visual capsule, per-item deltas or variation axes, and backend rejection checks. Do not instruct Lovart to forward execution, research, numbering, titles, or rejection prose into the image model. Keep the actual image-generation input to the shared visual capsule plus the current item delta.

Run the compression and pink-elephant audit in [prompt-architecture.md](references/prompt-architecture.md). Prefer positive replacement states over repeated forbidden nouns. Mention a high-cost forbidden mechanism once in backend rejection checks instead of repeating its synonyms throughout the visual prose.

### 10. Compile only executable language

Build visible clauses as:

`[subject] + [action or state] + [environment or carrier] + [composition] + [visible properties from the selected quality profile]`

Keep a sentence only when it changes the visible result, protects a high-cost lock, assigns a reference role, or controls Lovart execution and quality checks.
Remove unsupported praise such as “masterpiece”, “8K”, “ultra-detailed”, or “cinematic” when it lacks visible meaning.
Prefer structured specificity over keyword piles.

### 11. Check before delivery

Verify all of the following:

- Preserve the requested model, motifs, quantity, grouping, and supported format.
- Match the asset and quality profiles to the intended use.
- Keep reference roles isolated and within applicable caps.
- Include a complete tracking contract and non-random variation for batches; respect the selected visible, minimal, or internal metadata mode.
- Keep every requested image as an independent deliverable unless a design sheet was requested.
- Put any required pause inside the Lovart prompt, not in this conversation.
- Keep medium and rendering behavior ahead of broad genre labels in the visual capsule.
- Keep operational instructions, research text, names, numbering, and rejection checks out of the image-generation input.
- Remove repeated negatives, contradictions, metadata that could render as typography, and named concepts that are mentioned only to prohibit them.
- Include no fabricated research, source, interface fact, or completion claim.
- Include no placeholders, bracketed instructions, alternatives, or English duplicate.
- Make the continuity pack self-contained and list images that must be uploaded again.

## Output contract

Return one reusable Chinese artifact in the surface requested by the user. Use this default when no other surface is requested:

```text
Lovart Agent 提示词

【Lovart 界面建议】
模型：Nano Banana Pro
建议画幅：<one task-specific recommendation>
建议分辨率：<one task-specific recommendation>

【提示词】
<one complete ready-to-paste Chinese Lovart Agent prompt>

【续做包｜下次继续时完整贴回】
<self-contained common and asset-specific locks>
```

Replace every angle-bracketed instruction before delivery.
Treat interface values as recommendations unless the current Lovart surface was directly observed.
Keep model, aspect ratio, and resolution in `【Lovart 界面建议】`, not in the visual prose.
Use a fenced Markdown artifact when the user requests it.
Omit the continuity section whenever the user explicitly declines it or the task is a one-shot delivery with no continuation need. Include it for `extend` and otherwise when cross-session continuation is useful and not declined.
Do not force visible names or a visible numbered table when metadata mode is `internal`.
