#!/usr/bin/env python3
"""Deterministic structural lint for compiled Lovart Agent prompts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_route import load_manifest, validate_manifest


UNRESOLVED = (
    "同上次",
    "保持原样",
    "沿用之前",
    "以上次为准",
    "以最终报告为准",
    "以Lovart最终",
    "接着之前",
)

VISIBLE_GROUP_MARKERS = (
    "地域配额",
    "门派配额",
    "完整题材清单",
    "逐项清单",
    "命名清单",
    "十二个地域",
    "12个地域",
)

CONTINUITY_FIELDS = (
    "媒介：",
    "形状语言：",
    "主材料与表面变化：",
    "色彩关系：",
    "光结构：",
    "明度结构：",
    "细节密度：",
    "镜头或视图规则：",
    "文化、时代或技术规则：",
    "参考图编号与职责：",
    "下次必须重新上传的参考图或已批准成片：",
    "已用编号与名称：",
)


def _section(text: str, start: str, endings: tuple[str, ...]) -> str:
    if start not in text:
        return ""
    value = text.split(start, 1)[1]
    positions = [value.find(marker) for marker in endings if marker in value]
    positions = [position for position in positions if position >= 0]
    if positions:
        value = value[: min(positions)]
    return value.strip()


def _compact_length(value: str) -> int:
    return len(re.sub(r"\s+", "", value))


def lint_artifact(route: dict, text: str) -> tuple[list[str], list[str]]:
    errors, warnings = validate_manifest(route)

    if "【Lovart 界面建议】" not in text:
        errors.append("missing Lovart interface recommendations section")
    if "【提示词】" not in text:
        errors.append("missing prompt body marker")
        return errors, warnings

    interface_text = _section(text, "【Lovart 界面建议】", ("【提示词】",))
    body = _section(text, "【提示词】", ("【续做包｜下次继续时完整贴回】",))
    continuity = _section(text, "【续做包｜下次继续时完整贴回】", ())

    for value in route.get("interface", {}).values():
        if value and value not in interface_text:
            errors.append(f"interface recommendation missing manifest value: {value}")

    if route.get("route") == "explore":
        required_markers = ("【Agent执行合同】", "【调研与风格卡合同】", "【后台拒绝检查】")
    else:
        required_markers = ("【Agent执行合同】", "【共享视觉胶囊】", "【后台拒绝检查】")
    for marker in required_markers:
        if marker not in body:
            errors.append(f"missing required prompt marker: {marker}")
    if route.get("route") != "explore" and "【变化宪法】" not in body and "【当前单项差异】" not in body:
        errors.append("prompt body requires either variation constitution or current item delta")

    forbidden_ui_patterns = {
        "model name": re.compile(r"Nano\s*Banana|Gemini", re.IGNORECASE),
        "numeric aspect ratio": re.compile(r"(?<!\d)\d{1,2}\s*:\s*\d{1,2}(?!\d)"),
        "resolution label": re.compile(r"(?<![A-Za-z0-9])[248]\s*[Kk](?![A-Za-z0-9])|\d{3,4}\s*[x×]\s*\d{3,4}"),
    }
    for label, pattern in forbidden_ui_patterns.items():
        if pattern.search(body) or pattern.search(continuity):
            errors.append(f"{label} leaked outside interface recommendations")

    if "【共享视觉胶囊】" in body:
        capsule = _section(
            body,
            "【共享视觉胶囊】",
            ("【变化宪法】", "【当前单项差异】", "【后台拒绝检查】", "【参考图职责】"),
        )
        capsule_length = _compact_length(capsule)
        if capsule_length < 120:
            warnings.append(f"shared visual capsule is short ({capsule_length} chars); review completeness")
        if capsule_length > 450:
            errors.append(f"shared visual capsule exceeds 450 compact characters ({capsule_length})")

    if re.search(r"<[^>\n]{1,100}>", text):
        errors.append("unresolved angle-bracket placeholder found")
    for phrase in UNRESOLVED:
        if phrase in body or phrase in continuity:
            errors.append(f"unresolved continuity phrase found: {phrase}")

    count = str(route.get("deliverable_count", ""))
    execution = _section(body, "【Agent执行合同】", ("【共享视觉胶囊】", "【调研与风格卡合同】"))
    if count and count not in execution:
        errors.append("deliverable count is missing from Agent execution contract")

    if route.get("route") != "explore" and isinstance(route.get("deliverable_count"), int) and route["deliverable_count"] > 1:
        if "全局连续编号" not in execution:
            errors.append("multi-deliverable build requires one globally continuous numbering sequence")
        no_restart_phrases = ("不得在分组内重启", "不在分组内重启", "不因分组重启", "不得因分组重启")
        if not any(phrase in execution for phrase in no_restart_phrases):
            errors.append("numbering contract must forbid restarting inside groups")
        restarted_ranges = re.findall(r"(?:^|[、，；;\n])[^\n，；;]{0,12}0?1\s*[—–-]\s*10", execution)
        if len(restarted_ranges) > 1:
            errors.append("number ranges appear to restart inside multiple groups")

    if route.get("complexity") == "program" and route.get("pause_mode") == "dynamic-verification":
        coverage_phrases = ("每个独立方向至少一个", "覆盖全部独立方向", "覆盖所有独立方向")
        if not any(phrase in execution for phrase in coverage_phrases):
            errors.append("dynamic program verification must cover every independent direction across waves")

    if route.get("planning_owner") == "agent-planned" and route.get("metadata_mode") == "internal":
        if "完整追踪合同保留在Lovart执行层" not in execution:
            errors.append("agent-planned internal route must keep the complete tracking contract in Lovart execution layer")
        for marker in VISIBLE_GROUP_MARKERS:
            if marker in body:
                errors.append(f"host-invented visible planning marker found: {marker}")
        numbered_lines = re.findall(r"(?m)^\s*(?:\d{1,3}[.、)]|[-*]\s*\d{2,3}\b)", body)
        if len(numbered_lines) > 10:
            errors.append("agent-planned internal route contains an excessive visible numbered list")

    roles = route.get("reference_roles", [])
    if roles:
        if "【参考图职责】" not in body:
            errors.append("reference roles exist but prompt body lacks reference-role section")
        for role in roles:
            if role.get("id") not in body:
                errors.append(f"reference id missing from prompt body: {role.get('id')}")
    elif re.search(r"参考图\s*[0-9一二三四五六七八九]", body):
        errors.append("prompt assigns a reference image although route reference_roles is empty")

    wants_continuity = route.get("continuity_pack") is True
    if wants_continuity and not continuity:
        errors.append("route requires a continuity pack")
    if not wants_continuity and continuity:
        errors.append("route forbids a continuity pack")
    if continuity:
        for field in CONTINUITY_FIELDS:
            if field not in continuity:
                errors.append(f"continuity pack missing field: {field}")
        if route.get("route") != "extend" and "已用编号与名称：暂无" not in continuity:
            errors.append("initial build continuity pack must state 已用编号与名称：暂无")

    if "【后台拒绝检查】" in body:
        rejection = _section(body, "【后台拒绝检查】", ())
        if "图像模型" in rejection and "发送" in rejection:
            warnings.append("review rejection text to ensure it remains in Lovart execution layer")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    args = parser.parse_args()

    try:
        route = load_manifest(args.route)
        text = args.prompt.read_text(encoding="utf-8")
        errors, warnings = lint_artifact(route, text)
    except (OSError, UnicodeError, ValueError) as exc:
        errors, warnings = [str(exc)], []

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
