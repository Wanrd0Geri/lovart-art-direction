# Prompt Architecture and Compression

Use this reference to keep Lovart orchestration complete while keeping actual image prompts compact.

## Four layers

Compile four distinct layers:

1. **Agent execution contract**: model recommendation, deliverable count, format, research ownership, planning ownership, pause behavior, retries, metadata mode, and final reconciliation.
2. **Shared visual capsule**: the small set of visible invariants shared by every image: medium, rendering behavior, cultural system, shape or spatial logic, material response, light structure, and composition family.
3. **Item delta**: the current subject, state, environment, function, composition, and one or two planned differences.
4. **Backend rejection checks**: count errors, forbidden drift, text or layout leakage, reference-role leakage, structural failures, and quality regression.

Tell Lovart to send only layers 2 and 3 to the image model. Keep research prose, sources, workflow, numbering, names, batch checks, retry logic, and reporting in layers 1 and 4.

## Medium-first hierarchy

Order visible guidance as:

`medium and rendering behavior > cultural or genre system > subject > mood`

Do not lead with a broad market or genre label when it may imply an unwanted production tier. Labels such as `国漫`, `仙侠`, `游戏CG`, `暗黑神话`, or a work title may help route research, but they are not sufficient image-making instructions.

For a premium CG request, state visible medium behavior first, for example:

`高端写实CG环境成片，物理可信材质、自然全局光照、真实尺度和分层空气透视；文化与世界观来自中国仙侠。`

Avoid using `国漫风` as the leading operative style when the user wants top-tier UE or Blender realism. Preserve the Chinese animation or xianxia subject system through architecture, landscape, costume, ecology, color relationships, and narrative scale instead.

Engine or software names are secondary shorthand. Pair at most the useful names with visible material, light, geometry, and optical behavior; do not stack engine, renderer, resolution, and generic quality tokens as substitutes for art direction.

## Prompt budget

There is no universal character limit. Use these as compression targets, not hard caps:

- Agent execution contract: enough to control the run, commonly 400 to 800 Chinese characters.
- Shared visual capsule: commonly 150 to 350 Chinese characters.
- Item delta: commonly 50 to 150 Chinese characters.
- Backend rejection checks: five to eight grouped failure classes.

Large output count does not require a proportionally longer visible prompt. In `agent-planned` mode, provide a concise constitution, quotas, variation axes, and rejection rules; let Lovart build the detailed internal contract.

## Pink-elephant audit

Before delivery:

1. Remove any sentence that changes neither execution nor visible output.
2. State each constraint once at the layer where it belongs.
3. Replace a negative with a positive target state when that state is clear.
4. Keep a high-cost forbidden mechanism out of the positive pool and mention it once in backend rejection checks.
5. Do not enumerate many cultures, objects, effects, or styles only to prohibit them; state the authorized cultural system positively and reject drift as a class.
6. Remove names, titles, numbered headings, report text, and table labels from image-model inputs.
7. Check that allowed weather or actions do not imply a forbidden mechanism. Rain, for example, does not require electrical discharge.
8. Check for contradictions such as requesting a seamless black field while separately suggesting a black title band.
9. Compress repeated quality tokens into visible material, lighting, structural, or optical behavior.
10. Keep conditional optics conditional. Do not add rim light, shallow depth of field, grain, bloom, or lens flare merely because the user said `电影感`.

## Positive replacement patterns

Use positive replacements in the visual capsule and keep the short rejection rule in the backend.

| Risk | Visual capsule | Backend rejection |
| --- | --- | --- |
| Repeated forbidden weather effect | Describe the stable sky, motivated light, rain or fog, and reflections that should be visible | Reject the single forbidden mechanism if it appears |
| Cross-cultural drift | State the authorized cultural, geographic, material, and construction system | Reject unauthorized cultural drift |
| Typography leakage | Request an edge-to-edge visual-only image and remove names from item prompts | Reject visible typography, captions, title bands, or card layouts |
| Cheap genre rendering | Lead with the requested premium medium and visible render behavior; use genre as culture and subject | Reject low-tier stylization or medium drift |

## Regression cases

Use these cases when reviewing future changes:

1. A user requests a large one-shot batch with default resolution, no pause, no names, internal numbering, and no continuity pack. The artifact must honor every override while retaining internal checks.
2. A user requests `国漫仙侠` subject matter with premium UE or Blender rendering. The visual capsule must lead with high-end CG behavior and express `国漫仙侠` through culture and worldbuilding, not as a cheap rendering shortcut.
3. A user permits rain but forbids lightning. Describe rain through stable skylight, mist, wet materials, and reflection; mention lightning only once in backend rejection.
4. A reference image is assigned only to quality and finish. Do not inherit its identity, subject, age, costume, pose, or environment.
5. A user asks for a high-level constitution rather than hundreds of item descriptions. Use `agent-planned` mode and keep the complete tracking contract internal to Lovart.
