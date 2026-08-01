# Regression Cases

Run these cases after every material skill change. Validate both required behavior and forbidden output.

## 1. Lovart-owned large environment program

Request: 180 premium CG environment scenes; Lovart unifies the series; broad living-creator inspiration translated into visible traits; add Chinese xianxia worldbuilding.

Expected:

- `build`, `program`, `agent-planned`, `grouping_owner=lovart`, `metadata_mode=internal`;
- no host-invented named regions, factions, or 180-item list;
- concise shared visual capsule;
- creator names absent from operative image-model input;
- internal tracking, dynamic verification, and final reconciliation retained.
- verification proceeds in waves until every independent direction has an approved representative; do not release unverified directions after only the first five.
- include a self-contained continuity pack by program default unless the user explicitly declines it.

## 2. User-owned fixed groups

Request: 60 scenes split by the user into six named regions with ten scenes each.

Expected: preserve exact groups and quotas; do not replace names; visible or minimal metadata follows the user's review need; use one global sequence and never restart at 01 inside each region.

## 3. Uninterrupted internal batch

Request: large batch, no pause, no names, internal numbering, no continuity pack.

Expected: `pause_mode=uninterrupted`, internal checks retained, no visible item list, no continuity section.

## 4. Quality-only reference

Request: supplied image controls quality and finish only.

Expected: do not inherit identity, subject, age, costume, pose, environment, or specific composition.

## 5. Unassigned previous image

Request: current text follows an earlier generated image but does not authorize it as a reference.

Expected: `reference_roles=[]`; do not instruct the user to upload it or assign it a role.

## 6. Named living creator

Request: asks for a living creator's style without research.

Expected: `translate-visible-traits`; no creator name in operative model input; no fabricated attribution.

## 7. Premium CG plus genre label

Request: top-tier UE or Blender rendering with Chinese xianxia or donghua subject matter.

Expected: medium and visible render behavior lead; culture is expressed through worldbuilding; engine name is supporting shorthand only.

## 8. Aspect-ratio isolation

Request: explicit 16:9 and 2K.

Expected: both appear only under interface recommendations; neither appears in prompt body or continuity pack.

## 9. Empty verification prevention

Request: two outputs.

Expected: both are verification results; no pause after all requested outputs are complete.

## 10. Missing continuation evidence

Request: extend a high-fidelity character batch without approved images or a self-contained pack.

Expected: ask for the missing evidence; do not promise identity-level continuity.

## 11. Continuity integrity

Request: initial program before any generation.

Expected: pack states `已用编号与名称：暂无`; reject `以最终报告为准`, `同上次`, and other unresolved references.

## 12. Count reconciliation

Request: any multi-deliverable batch with a failed item.

Expected: report the failed and missing identifiers explicitly; regenerate failed items only; never silently reduce count.

## Forward-test protocol

Use clean-context agents as ordinary users of the skill. Do not reveal the suspected bug, expected answer, or previous failed output.
Test at least one `explore`, two `build` programs with different planning owners, one multi-reference `controlled` build, and one `extend` case.
Inspect the raw artifact and route manifest, not only the final prose.
On Windows, use `scripts/validate_artifact.ps1`; do not treat unavailable bare `python` or `py -3` as proof that validation cannot run.
