#!/usr/bin/env python3
"""Validate the strict routing manifest used by lovart-art-direction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ENUMS = {
    "route": {"explore", "build", "extend"},
    "complexity": {"simple", "controlled", "program"},
    "research_owner": {"research-by-host", "research-by-lovart", "no-research"},
    "research_followup": {"research-then-review", "research-then-execute", "none"},
    "planning_owner": {"host-specified", "agent-planned", "hybrid"},
    "grouping_owner": {"user", "lovart", "shared", "none"},
    "metadata_mode": {"visible", "minimal", "internal"},
    "pause_mode": {"dynamic-verification", "uninterrupted", "none"},
    "named_direction_handling": {"none", "translate-visible-traits", "verified-research"},
    "continuity_reason": {"program-default", "extend-required", "user-required", "user-declined", "one-shot-not-useful"},
}

REQUIRED = {
    *ENUMS,
    "continuity_pack",
    "continuation_source",
    "deliverable_count",
    "asset_types",
    "intended_use",
    "user_defined_groups",
    "reference_roles",
    "interface",
    "assumptions",
}

REFERENCE_ROLES = {
    "identity",
    "pose",
    "composition",
    "environment",
    "material",
    "style-axis",
    "quality-finish",
}

REFERENCE_CLASSES = {
    "general",
    "high-fidelity-object",
    "character-consistency",
    "style-reference",
}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read UTF-8 JSON manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("route manifest must be a JSON object")
    return value


def validate_manifest(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED - data.keys())
    unknown = sorted(data.keys() - REQUIRED)
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if unknown:
        errors.append("unknown fields: " + ", ".join(unknown))

    for field, allowed in ENUMS.items():
        value = data.get(field)
        if value not in allowed:
            errors.append(f"{field} must be one of {sorted(allowed)}; got {value!r}")

    if not isinstance(data.get("continuity_pack"), bool):
        errors.append("continuity_pack must be boolean")
    if not isinstance(data.get("continuation_source"), str):
        errors.append("continuation_source must be a string")
    count = data.get("deliverable_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        errors.append("deliverable_count must be an integer greater than zero")

    asset_types = data.get("asset_types")
    if not isinstance(asset_types, list) or not asset_types or not all(isinstance(x, str) and x.strip() for x in asset_types):
        errors.append("asset_types must be a non-empty array of non-empty strings")
    if not isinstance(data.get("intended_use"), str) or not data.get("intended_use", "").strip():
        errors.append("intended_use must be a non-empty string")

    for field in ("user_defined_groups", "reference_roles", "assumptions"):
        if not isinstance(data.get(field), list):
            errors.append(f"{field} must be an array")

    if isinstance(data.get("assumptions"), list) and not all(
        isinstance(x, str) and x.strip() for x in data["assumptions"]
    ):
        errors.append("assumptions must contain only non-empty strings")

    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append("interface must be an object")
    else:
        expected = {"model", "aspect_ratio", "resolution"}
        if set(interface) != expected:
            errors.append("interface must contain exactly model, aspect_ratio, and resolution")
        for key in expected:
            if not isinstance(interface.get(key), str) or not interface.get(key, "").strip():
                errors.append(f"interface.{key} must be a non-empty string")

    roles = data.get("reference_roles")
    if isinstance(roles, list):
        seen_pairs: set[tuple[str, str]] = set()
        class_by_id: dict[str, str] = {}
        for index, role in enumerate(roles):
            prefix = f"reference_roles[{index}]"
            if not isinstance(role, dict):
                errors.append(f"{prefix} must be an object")
                continue
            if set(role) != {"id", "role", "capability_class", "allow", "keep_neutral"}:
                errors.append(f"{prefix} must contain exactly id, role, capability_class, allow, keep_neutral")
            role_id = role.get("id")
            if not isinstance(role_id, str) or not role_id.strip():
                errors.append(f"{prefix}.id must be a non-empty string")
            role_name = role.get("role")
            if role_name not in REFERENCE_ROLES:
                errors.append(f"{prefix}.role must be one of {sorted(REFERENCE_ROLES)}")
            capability_class = role.get("capability_class")
            if capability_class not in REFERENCE_CLASSES:
                errors.append(f"{prefix}.capability_class must be one of {sorted(REFERENCE_CLASSES)}")
            if isinstance(role_id, str) and role_id.strip() and role_name in REFERENCE_ROLES:
                pair = (role_id, role_name)
                if pair in seen_pairs:
                    errors.append(f"duplicate reference id-role pair: {role_id}/{role_name}")
                seen_pairs.add(pair)
                previous_class = class_by_id.get(role_id)
                if previous_class is not None and previous_class != capability_class:
                    errors.append(f"reference {role_id} uses inconsistent capability classes")
                elif capability_class in REFERENCE_CLASSES:
                    class_by_id[role_id] = capability_class
            if role_name == "identity" and capability_class != "character-consistency":
                errors.append(f"{prefix} identity role requires capability_class=character-consistency")
            if role_name == "style-axis" and capability_class != "style-reference":
                errors.append(f"{prefix} style-axis role requires capability_class=style-reference")
            for key in ("allow", "keep_neutral"):
                value = role.get(key)
                if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
                    errors.append(f"{prefix}.{key} must be a non-empty array of strings")

    route = data.get("route")
    research = data.get("research_owner")
    followup = data.get("research_followup")
    planning = data.get("planning_owner")
    grouping = data.get("grouping_owner")
    groups = data.get("user_defined_groups")
    pause = data.get("pause_mode")

    if route == "extend":
        if data.get("continuity_pack") is not True:
            errors.append("route=extend requires continuity_pack=true")
        if not str(data.get("continuation_source", "")).strip():
            errors.append("route=extend requires a non-empty continuation_source")
        if data.get("continuity_reason") not in {"extend-required", "user-required"}:
            errors.append("route=extend requires continuity_reason=extend-required or user-required")
    elif str(data.get("continuation_source", "")).strip():
        warnings.append("continuation_source is ignored unless route=extend")

    if research == "no-research" and followup != "none":
        errors.append("research_owner=no-research requires research_followup=none")
    if research in {"research-by-host", "research-by-lovart"} and followup == "none":
        errors.append("a research mode requires research_followup other than none")

    if planning == "agent-planned" and grouping not in {"lovart", "none"}:
        errors.append("planning_owner=agent-planned requires grouping_owner=lovart or none")
    if grouping == "lovart" and isinstance(groups, list) and groups:
        errors.append("grouping_owner=lovart requires empty user_defined_groups")
    if grouping == "user" and isinstance(groups, list) and not groups:
        errors.append("grouping_owner=user requires user_defined_groups")

    if data.get("complexity") == "program" and pause == "none" and isinstance(count, int) and count >= 3:
        errors.append("program with at least three deliverables requires dynamic-verification or uninterrupted pause mode")
    if isinstance(count, int) and count < 3 and pause == "dynamic-verification":
        errors.append("fewer than three deliverables must not create a dynamic verification pause; use pause_mode=none")
    if isinstance(count, int) and count >= 6 and data.get("complexity") == "simple":
        warnings.append("six or more deliverables are rarely complexity=simple; review routing")

    continuity = data.get("continuity_pack")
    continuity_reason = data.get("continuity_reason")
    if continuity_reason in {"program-default", "extend-required", "user-required"} and continuity is not True:
        errors.append(f"continuity_reason={continuity_reason} requires continuity_pack=true")
    if continuity_reason in {"user-declined", "one-shot-not-useful"} and continuity is not False:
        errors.append(f"continuity_reason={continuity_reason} requires continuity_pack=false")
    if data.get("complexity") == "program" and continuity is False and continuity_reason != "user-declined":
        errors.append("program may omit continuity only when the user explicitly declined it")
    if continuity_reason == "one-shot-not-useful" and data.get("complexity") == "program":
        errors.append("one-shot-not-useful is not valid for a program")

    if data.get("named_direction_handling") == "verified-research" and research == "no-research":
        errors.append("verified-research named direction handling requires a research mode")

    if isinstance(roles, list):
        unique_ids = {item.get("id") for item in roles if isinstance(item, dict) and isinstance(item.get("id"), str)}
        object_ids = {
            item.get("id") for item in roles if isinstance(item, dict) and item.get("capability_class") == "high-fidelity-object"
        }
        identity_ids = {
            item.get("id") for item in roles if isinstance(item, dict) and item.get("capability_class") == "character-consistency"
        }
        style_ids = {
            item.get("id") for item in roles if isinstance(item, dict) and item.get("capability_class") == "style-reference"
        }
        if len(unique_ids) > 14:
            errors.append("reference count exceeds dated API snapshot total of 14")
        if len(object_ids) > 6:
            errors.append("high-fidelity object reference count exceeds dated API snapshot limit of 6")
        if len(identity_ids) > 5:
            errors.append("identity reference count exceeds dated API snapshot character-consistency limit of 5")
        if len(style_ids) > 3:
            errors.append("style-axis reference count exceeds dated API snapshot style-reference limit of 3")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest(args.manifest)
        errors, warnings = validate_manifest(data)
    except ValueError as exc:
        errors, warnings = [str(exc)], []

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
