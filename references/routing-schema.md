# Routing Schema

Create a UTF-8 JSON object with every required field before compiling the Lovart artifact.
The manifest is execution metadata and must not appear in the image.

## Required fields

| Field | Allowed value |
| --- | --- |
| `route` | `explore`, `build`, `extend` |
| `complexity` | `simple`, `controlled`, `program` |
| `research_owner` | `research-by-host`, `research-by-lovart`, `no-research` |
| `research_followup` | `research-then-review`, `research-then-execute`, `none` |
| `planning_owner` | `host-specified`, `agent-planned`, `hybrid` |
| `grouping_owner` | `user`, `lovart`, `shared`, `none` |
| `metadata_mode` | `visible`, `minimal`, `internal` |
| `pause_mode` | `dynamic-verification`, `uninterrupted`, `none` |
| `continuity_pack` | boolean |
| `continuity_reason` | `program-default`, `extend-required`, `user-required`, `user-declined`, `one-shot-not-useful` |
| `continuation_source` | non-empty string for `extend`, otherwise empty string |
| `deliverable_count` | integer greater than zero |
| `asset_types` | non-empty array |
| `intended_use` | non-empty string |
| `user_defined_groups` | array, empty when none were supplied |
| `reference_roles` | array of explicit image-role objects |
| `interface` | object containing `model`, `aspect_ratio`, and `resolution` |
| `named_direction_handling` | `none`, `translate-visible-traits`, `verified-research` |
| `assumptions` | array of reversible non-critical assumptions |

Every `reference_roles` item must contain:

```json
{
  "id": "参考图1",
  "role": "identity|pose|composition|environment|material|style-axis|quality-finish",
  "capability_class": "general|high-fidelity-object|character-consistency|style-reference",
  "allow": ["authorized attributes"],
  "keep_neutral": ["unassigned attributes"]
}
```

## Hard consistency rules

- `route=extend` requires `continuity_pack=true` and a supplied self-contained continuity source.
- `complexity=program` defaults to `continuity_pack=true` with `continuity_reason=program-default`; only an explicit user refusal may use `user-declined` and omit the pack.
- `user-required`, `program-default`, and `extend-required` require `continuity_pack=true`; `user-declined` and `one-shot-not-useful` require `continuity_pack=false`.
- `research_owner=no-research` requires `research_followup=none`; every research mode requires a non-`none` follow-up.
- `complexity=program` requires `planning_owner` other than an unresolved value and `pause_mode` other than `none` unless every deliverable is itself a verification result.
- Fewer than three deliverables use `pause_mode=none`; all requested outputs are verification results, so an additional verification pause would be empty.
- `planning_owner=agent-planned` requires `grouping_owner=lovart` or `none`.
- `grouping_owner=lovart` requires empty `user_defined_groups` unless the user supplied only high-level quotas that Lovart must expand.
- `metadata_mode=internal` forbids a visible complete item list.
- Six or more deliverables normally require `controlled` or `program`; count alone does not override asset or reference complexity.
- A reference may have multiple roles only when the user explicitly authorized each role. Otherwise split the roles or ask.
- Repeated roles for one reference must use one consistent capability class. Check total references and every applicable capability class separately.
- A previous conversational image is not a reference until the user assigns it.
- Living creator or studio names require `translate-visible-traits` or `verified-research`; never forward the names as operative model style instructions.

## Question gate

Ask one consolidated question only if one of these remains materially unresolved:

- deliverable count;
- identity owner;
- reference ownership;
- grouping ownership;
- research ownership when attribution is requested;
- continuation source;
- a choice that changes the project direction rather than a reversible implementation detail.

When the user says Lovart should unify or decide the series, resolve the state as:

```json
{
  "planning_owner": "agent-planned",
  "grouping_owner": "lovart",
  "metadata_mode": "internal"
}
```

Do not ask the host to invent regions, factions, names, or an item list after this state is set.

## Interface state

Interface values are recommendations unless the current Lovart surface was directly observed.
Use the requested value when supported; otherwise recommend the nearest verified option and disclose uncertainty outside the visual prose.
