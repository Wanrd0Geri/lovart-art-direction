# Reference Roles and Continuity

Treat every uploaded image as evidence with a narrow, explicit role.
Never treat “reference image” as permission to copy every visible attribute.

## Attribute allowlist

| Role | Allow | Keep neutral unless separately assigned |
| --- | --- | --- |
| Identity | face, hair, body type, age impression, explicitly assigned identity clothing | pose, camera, environment, light |
| Pose | limb configuration, action, contact, gaze direction | identity, clothing, environment, style |
| Composition | placement, scale, crop, occlusion, depth, negative space | identity, material, palette, subject matter |
| Environment | terrain, architecture, weather, environmental materials, props | character identity, pose, camera changes |
| Material | properties and variation of the named surface | people, architecture, composition, palette, light |
| Style axis | explicitly named medium, shape, edge, material, color, light, or surface axis | every unassigned visual attribute |
| Quality and finish | crop completeness, presentation cleanliness, material fidelity, light structure, optical behavior, render finish | identity, face, age, costume, subject, pose, environment, named design |

Keep all unassigned attributes neutral.
Resolve conflicts by assigned roles, not by averaging images.
Ignore interface chrome, arrows, watermarks, captions, and irrelevant text.

## Capability gates

Use this Google Gemini 3 Pro Image API snapshot, checked 2026-08-01 from
<https://ai.google.dev/gemini-api/docs/image-generation>:

| Check | Published maximum |
| --- | --- |
| Total reference images | 14 |
| High-fidelity object images | 6 |
| Character-consistency images | 5 |
| Style-reference images | 3 |

Check the total and every applicable category separately.
For each check, use the smaller of the dated API snapshot and the currently verified Lovart surface limit.
Do not claim the API snapshot is a Lovart interface capability.
When the current surface cannot be inspected, use the snapshot only as a conservative ceiling.
When references exceed the applicable ceiling, identify the affected images and ask which to keep, or split roles into sequential stages.

## Continuity pack

Use a continuity pack when cross-session continuation, identity restoration, or later extension is useful. Omit it when the user explicitly declines it or requests a one-shot delivery with no continuation need. An explicit user choice overrides program-level defaults.

Write a self-contained Chinese pack with these common fields:

```text
媒介：
形状语言：
主材料与表面变化：
色彩关系：
光结构：
明度结构：
细节密度：
镜头或视图规则：
文化、时代或技术规则：
调研依据与来源链接：
参考图编号与职责：
下次必须重新上传的参考图或已批准成片：
已用编号与名称：
```

Add only the relevant asset fields:

| Asset | Additional fields |
| --- | --- |
| Character | face anchor, body type, silhouette, core clothing, equipment placement, allowed variation |
| Environment | geography, building function, circulation, water, scale, landmark, allowed variation |
| VFX | energy source, hierarchy, trajectory, color relationship, environmental feedback, current stage |
| Creature | anatomy, locomotion, proportions, surface, ecology |
| Prop | function, construction, scale, material, craft, state-appropriate wear, grip relation |

Do not use unresolved references such as `同上次` or `保持原样`.
State that text cannot replace high-fidelity image evidence.
List every face, complex costume, creature body, prop design, or approved output that must be uploaded again.
When those images are missing, restore only textual design rules and do not promise identity-level consistency.

## Restore and update

Apply this priority:

1. Current explicit user change.
2. Current image explicitly assigned by the user.
3. Existing continuity-pack field.
4. Skill default.

Update only fields changed through text or an explicitly assigned current image.
Do not infer that every incidental difference in a new image is a requested change.
Preserve all other high-cost locks, reference roles, and numbering rules.
Return a complete replacement continuity pack after every extension unless the user explicitly declines continuity output for that extension.
