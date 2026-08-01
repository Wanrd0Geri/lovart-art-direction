# Asset Profiles

Choose profiles by intended use, not by nouns alone.
Use multiple rows for mixed projects, but activate only relevant dimensions.

| Asset and use | Default format | Design dimensions | Common failures to prevent |
| --- | --- | --- | --- |
| Environment, architecture, world keyframe | 16:9 | terrain, climate, function, circulation, scale, structure, material, depth layers | decorative noise, impossible access or load paths, repeated landmarks |
| Full-body single character | 3:4 | silhouette, body type, identity, clothing hierarchy, material, equipment, cultural source | vague identity, random accessories, proportion drift |
| Bust portrait | 4:5 | face, hair, identity anchor, expression, upper costume, lighting | over-smoothed skin, same-face drift, costume detached from role |
| Character turnaround or design sheet | 16:9 or 3:2 | front-side-back consistency, proportions, garment construction, equipment placement | identity drift between views, dramatic light hiding structure |
| Creature or spirit beast | 3:4 | anatomy, silhouette, locomotion, surface, ecological adaptation | anatomy unable to move, false detail masking body logic |
| Giant creature in environment | 16:9 | scale evidence, occlusion, environmental contact, damage radius, spatial relation | unsupported scale, floating contact, no environmental effect |
| Prop, weapon, ritual object | 4:3 or 1:1 | function, construction, material, grip scale, craft, state-appropriate wear | function disconnected from form, implausible weight or grip |
| Integrated scene VFX | 16:9 | source, trajectory, scale, illumination, smoke, debris, environmental feedback | pasted glow, no contact with air, ground, or subject |
| Isolated VFX exploration | 1:1 or 4:3 | core, body layer, edge, particles, color relation, dissipation | flat hierarchy, meaningless particles, unknown scale |
| Staged VFX design sheet | 16:9 | initiation, formation, peak, dissipation, causal continuity | unrelated stages, changing camera or subject position |

Treat these formats as recommendations.
Honor an explicit user format when the current Lovart surface supports it.
When it does not, recommend the nearest available format and describe the difference.

For premium CG assets, state the medium before the genre. For example, compile `high-end realistic CG environment with physically grounded materials and natural global illumination; Chinese xianxia worldbuilding` rather than leading with `国漫仙侠风`. Use the cultural label to control architecture, landscape, ecology, costume, symbolism, and narrative scale, not to imply simplified animation rendering.

For a black-background full-body character, use the full-body profile plus the conditional quality rules in `quality-profiles.md`. For a premium CG environment, use the environment profile plus the premium CG environment condition there.

Use this dated Nano Banana Pro API snapshot only as a capability reference, not as proof of Lovart UI support:

`1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9` — checked 2026-08-01.

For an unsupported final ratio, generate at the nearest supported ratio first.
Add crop, outpaint, or layout adaptation only when the current Lovart surface exposes that operation.
