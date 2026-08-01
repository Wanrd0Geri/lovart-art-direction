# Build Compiler

Use for `route=build`. Apply the complexity selected in the route manifest.

## Simple

Compile the goal, necessary reference roles, matching asset and quality profile, one shared visual capsule, one current item delta, and direct generation instruction.
Do not force a variation matrix, visible tracking table, verification pause, or continuity pack when the route does not require them.

## Controlled

Compile fixed design rules, explicit reference roles, useful variation axes, numbering for multiple independent deliverables, rejection checks, and a continuity pack when requested.
Use identity or construction locks where drift would be costly.

## Program

Use for large batches, multiple directions, worldbuilding systems, or mixed asset programs.
Include a self-contained continuity pack by default. Omit it only when the user explicitly declines it.

### Execution contract

State:

- exact total deliverable count;
- one independent image per deliverable unless the user requested a design sheet;
- planning owner, grouping owner, and metadata mode;
- one globally unique continuous numbering sequence and final reconciliation; never restart numbering inside a group, region, faction, batch, or extension;
- dynamic verification or uninterrupted behavior;
- failed-number-only regeneration;
- no quality reduction in later batches.

### Planning modes

- `host-specified`: compile the supplied groups and items without expanding beyond the authorized scope.
- `hybrid`: lock user-confirmed groups or representative items; let Lovart complete the rest within fixed quotas.
- `agent-planned`: give Lovart the fixed world constitution, asset quota, three or four variation axes, and forbidden drift. Require Lovart to build the complete item-level tracking contract internally. Do not invent a visible named taxonomy.

### Variation constitution

Separate:

1. fixed attributes: medium, world rules, cultural family, material system, reference locks, within-group quality;
2. planned variation: choose three or four reasonably independent axes such as geography, function, civilization state, narrative state, occupation, technique phase, or camera state;
3. forbidden drift: unauthorized culture, medium, identity, core material, reference-role changes, repeated composition, or count reduction.

Weather, time of day, and palette may support variation but cannot be the sole difference between directions.
When Lovart owns planning, name only the axes and authorized quotas, not every axis value or item.

### Dynamic verification gate

- Fewer than three outputs: all outputs are verification results; do not create an empty pause.
- One direction with at least three outputs: verify the three highest-risk items.
- Multiple independent directions: verify at least one item from every direction.
- More than five directions: verify at most five directions per wave and pause between waves.
- Continue verification waves until every independent direction has at least one approved representative; a first wave of five does not release unverified remaining directions.
- Prefer complex materials, unusual construction, extreme scale, multiple references, or high-intensity VFX.
- After rejection, update the shared rule that caused the failure and regenerate only affected verification items.
- When `pause_mode=uninterrupted`, remove approval pauses but retain internal checks and retries.

### Batch checks

For every batch:

- reconcile requested, completed, failed, missing, and remaining numbers;
- detect repeated composition, landmark, silhouette, subject function, and VFX topology;
- verify culture, medium, materials, identity, quality, and reference roles;
- reject visible metadata, captions, title bands, card layouts, and UI;
- compare late-batch quality against approved early outputs;
- regenerate failed numbers only.

### Research inside build

Apply the manifest's research owner.
Research exists to extract executable design logic, not to decorate prompts with names.
For verified cases, separate confirmed facts, uncertainty, executable attributes, and non-copyable expression.
Do not infer tools, engines, authors, or consensus from appearance alone.
