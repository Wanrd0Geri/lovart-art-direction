# Batch Contract

Use a tracking contract to prevent silent count reduction and uncontrolled repetition. Its metadata may be visible, minimal, or internal according to the user's request.

## Metadata modes

Choose exactly one:

| Mode | Use when | Contract surface |
| --- | --- | --- |
| `visible` | The user wants a reviewable plan or named assets | Show number, optional name, group, axis values, and unique delta in chat |
| `minimal` | The user wants count visibility without special naming | Show number, group or function, and unique delta; omit names |
| `internal` | The user wants only a high-level brief or names may leak into images | Lovart keeps the complete contract in backend state and reports only reconciliation totals |

Metadata is never raster content. Do not forward numbers, names, group titles, table headers, research labels, or status text into the image model unless the user explicitly requests typography as part of the artwork.

## Tracking list

For `visible` mode, use columns equivalent to:

```text
| 编号 | 名称 | 分组 | 各轴取值 | 唯一差异点 |
```

Require:

- One independent delivered image per number.
- A multi-view or multi-stage image only when the user explicitly requests a design sheet.
- Continuous numbering across batches and extensions.
- A final reconciliation of requested, completed, failed, and missing numbers.
- Explicit acknowledgement of missing outputs instead of silent count reduction.

Names are optional. In `minimal` and `internal` modes, identifiers exist only for delivery tracking and must not become image titles, captions, filename-like text, title bands, or card layouts.

Do not use a collage to substitute for multiple independently requested images.

## Dynamic verification gate

- For fewer than three final outputs, treat all as verification results; do not create an empty pause when nothing remains.
- For one style or faction with at least three outputs, select the three highest-risk items.
- For multiple styles or factions, select at least one item from every independent direction.
- For more than five directions, verify at most five directions per wave and pause between waves.
- Never select more verification items than the final requested count.
- Within a direction, prefer complex materials, multiple characters, multiple references, extreme scale, unusual construction, or high-intensity VFX.

Do not select only the easiest subjects.
After approval, continue the remaining numbers.
After rejection, update the shared rule that caused the failure and regenerate only affected verification items before release.

## Batching

- Default to one high-quality image per generation action unless the current Lovart surface reliably supports another mode.
- Keep every requested image independent.
- Allow multiple views in one image only for a requested design sheet and only while every view remains readable.
- Choose batch size from current Lovart plan, interface, and observed task stability.
- Do not hard-code a universal Lovart batch maximum.
- Keep numbering continuous and never restart at `01` between batches.
- When the user requests immediate full generation, remove the wait but retain per-batch checks.

For an unattended full run, keep checks and retry decisions in Lovart's execution layer. Do not pause for approval, do not emit sample gates, and do not lower material, structural, optical, or compositional quality in later batches.

## Per-batch checks

- Reconcile number completeness.
- Check within-group medium, culture, materials, identity, and quality-system consistency.
- Ensure differences between groups exceed weather or palette swaps.
- Detect repeated composition, landmark, silhouette, subject function, or VFX topology.
- Recheck the selected asset and quality profiles.
- Detect reference-role leakage.
- Detect visible metadata, typography, captions, title bands, card layouts, or other execution-layer leakage.
- Detect quality regression between early and late batches.

Regenerate failed numbers only.
Do not discard already approved outputs.
