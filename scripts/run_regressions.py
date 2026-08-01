#!/usr/bin/env python3
"""Self-contained regression tests for lovart-art-direction route and prompt lint."""

from __future__ import annotations

import copy
import sys

from lint_prompt import lint_artifact
from validate_route import validate_manifest


BASE_ROUTE = {
    "route": "build",
    "complexity": "program",
    "research_owner": "no-research",
    "research_followup": "none",
    "planning_owner": "agent-planned",
    "grouping_owner": "lovart",
    "metadata_mode": "internal",
    "pause_mode": "dynamic-verification",
    "continuity_pack": True,
    "continuity_reason": "program-default",
    "continuation_source": "",
    "deliverable_count": 180,
    "asset_types": ["environment"],
    "intended_use": "游戏环境概念设计",
    "user_defined_groups": [],
    "reference_roles": [],
    "interface": {
        "model": "Nano Banana Pro",
        "aspect_ratio": "16:9",
        "resolution": "2K",
    },
    "named_direction_handling": "translate-visible-traits",
    "assumptions": [],
}

VALID_PROMPT = """Lovart Agent 提示词

【Lovart 界面建议】
模型：Nano Banana Pro
建议画幅：16:9
建议分辨率：2K

【提示词】
【Agent执行合同】
交付180张独立环境场景图。由Lovart统一规划分组与逐项差异，完整追踪合同保留在Lovart执行层；使用全局连续编号，不得因分组重启；分波校验直至每个独立方向至少一个代表获得批准，再分批完成，失败项单独重做并最终核对完成、失败和缺失数量。

【共享视觉胶囊】
高端写实CG环境成片，以物理可信的几何、材质响应、自然全局光照、分层空气透视和清晰焦点层级表现巨大而可探索的原创世界。东方玄幻通过山水地理、礼制空间、木石青铜工程、修炼文明和灵性生态进入场景；科技悬疑通过埋藏于古文明内部的精密传导结构与环境谜团呈现。人物仅作为尺度和社会活动证据，环境保持主体地位。

【变化宪法】
固定高端写实CG媒介、东方玄幻文化系统、环境主导和材料可信度。Lovart内部以地理、场景功能、文明状态和叙事状态建立相互独立的变化轴，并为每个编号记录唯一差异；天气和色调只作辅助，不得替代结构变化。

【后台拒绝检查】
拒绝数量缩减、重复构图、文化漂移、无功能建筑、材料塑料化、效果缺少环境反馈、可见文字与执行元数据、参考职责泄漏和后半批质量下降。只重做失败编号。

【续做包｜下次继续时完整贴回】
媒介：高端写实CG环境成片。
形状语言：自然地貌与功能性巨构形成尺度对比。
主材料与表面变化：木、石、青铜与地域材料按照环境状态呈现差异。
色彩关系：克制的大地底色与少量灵性能量色。
光结构：具有来源的自然光、环境反弹和空气散射。
明度结构：地标、路径和尺度参照保持清晰。
细节密度：焦点最高，支撑区域逐级降低。
镜头或视图规则：环境主导，路径可读，人物只作尺度参照。
文化、时代或技术规则：原创东方玄幻文明与埋藏式精密遗迹共存。
参考图编号与职责：无。
下次必须重新上传的参考图或已批准成片：首次生成后上传所有已批准校验图；当前无已批准成片。
已用编号与名称：暂无；计划总数180。
"""


def expect(name: str, should_pass: bool, route: dict, prompt: str | None = None) -> tuple[bool, str]:
    if prompt is None:
        errors, _ = validate_manifest(route)
    else:
        errors, _ = lint_artifact(route, prompt)
    passed = not errors
    ok = passed is should_pass
    detail = "PASS" if ok else f"FAIL expected={should_pass} actual={passed} errors={errors}"
    return ok, f"{name}: {detail}"


def main() -> int:
    cases: list[tuple[str, bool, dict, str | None]] = []
    cases.append(("valid lovart-owned program", True, BASE_ROUTE, VALID_PROMPT))

    invalid_groups = copy.deepcopy(BASE_ROUTE)
    invalid_groups["user_defined_groups"] = ["区域A"]
    cases.append(("lovart-owned route rejects host groups", False, invalid_groups, None))

    visible_regions = VALID_PROMPT.replace("【变化宪法】", "【地域配额】\n十二个地域，每个地域十五张。\n\n【变化宪法】")
    cases.append(("agent-planned prompt rejects visible regions", False, BASE_ROUTE, visible_regions))

    leaked_ratio = VALID_PROMPT.replace("高端写实CG环境成片，以物理", "16:9高端写实CG环境成片，以物理")
    cases.append(("aspect ratio leakage is blocked", False, BASE_ROUTE, leaked_ratio))

    unresolved = VALID_PROMPT.replace("已用编号与名称：暂无；计划总数180。", "已用编号与名称：以最终报告为准。")
    cases.append(("unresolved continuity is blocked", False, BASE_ROUTE, unresolved))

    incomplete_coverage = VALID_PROMPT.replace(
        "分波校验直至每个独立方向至少一个代表获得批准",
        "先选择五个不同方向进行校验",
    )
    cases.append(("verification must cover every direction", False, BASE_ROUTE, incomplete_coverage))

    restarted_numbering = VALID_PROMPT.replace(
        "使用全局连续编号，不得因分组重启",
        "雪原01—10、盐海01—10、火山01—10、竹泽01—10、沙漠01—10、地宫01—10",
    )
    cases.append(("numbering may not restart by group", False, BASE_ROUTE, restarted_numbering))

    invented_reference = VALID_PROMPT.replace("由Lovart统一规划", "参考图1控制构图。由Lovart统一规划")
    cases.append(("unassigned previous reference is blocked", False, BASE_ROUTE, invented_reference))

    no_continuity_route = copy.deepcopy(BASE_ROUTE)
    no_continuity_route.update({"continuity_pack": False, "continuity_reason": "user-declined", "pause_mode": "uninterrupted"})
    no_continuity_prompt = VALID_PROMPT.split("【续做包｜下次继续时完整贴回】", 1)[0].rstrip()
    cases.append(("uninterrupted no-continuity program", True, no_continuity_route, no_continuity_prompt))

    bad_research = copy.deepcopy(BASE_ROUTE)
    bad_research.update({"research_owner": "research-by-host", "research_followup": "none"})
    cases.append(("research requires followup", False, bad_research, None))

    explore_route = copy.deepcopy(BASE_ROUTE)
    explore_route.update(
        {
            "route": "explore",
            "complexity": "controlled",
            "research_owner": "research-by-lovart",
            "research_followup": "research-then-review",
            "planning_owner": "agent-planned",
            "grouping_owner": "none",
            "metadata_mode": "visible",
            "pause_mode": "dynamic-verification",
            "continuity_pack": False,
            "continuity_reason": "one-shot-not-useful",
            "deliverable_count": 3,
            "named_direction_handling": "verified-research",
        }
    )
    explore_prompt = """Lovart Agent 提示词

【Lovart 界面建议】
模型：Nano Banana Pro
建议画幅：16:9
建议分辨率：2K

【提示词】
【Agent执行合同】
调研并交付3张可比较的风格卡。先完成有来源的调研与差异化设计，不进入图像生成；研究结论交付后暂停等待选择。

【调研与风格卡合同】
每个方向记录媒介、形状、材料、色彩、光与明度、细节密度、构造功能、文化规则、可靠来源和不可复制表达。区分确认事实、未确认信息与设计综合，三个方向必须存在结构差异。

【后台拒绝检查】
拒绝虚构来源、把人物或作品名称作为模型风格词、只靠天气和色调区分方向、未确认工具归因，以及在方向获批前启动生成。
"""
    cases.append(("valid explore research route", True, explore_route, explore_prompt))

    fixed_route = copy.deepcopy(BASE_ROUTE)
    fixed_route.update(
        {
            "planning_owner": "host-specified",
            "grouping_owner": "user",
            "metadata_mode": "visible",
            "deliverable_count": 60,
            "user_defined_groups": ["雪原10", "盐海10", "火山10", "竹泽10", "沙漠10", "地宫10"],
            "reference_roles": [
                {
                    "id": "参考图1",
                    "role": "quality-finish",
                    "capability_class": "style-reference",
                    "allow": ["材质完成度", "光照质量"],
                    "keep_neutral": ["构图", "建筑", "人物", "地形", "色彩"],
                }
            ],
        }
    )
    fixed_prompt = VALID_PROMPT.replace(
        "交付180张独立环境场景图。由Lovart统一规划分组与逐项差异，完整追踪合同保留在Lovart执行层；使用全局连续编号，不得因分组重启；分波校验直至每个独立方向至少一个代表获得批准",
        "交付60张独立环境场景图。用户锁定雪原、盐海、火山、竹泽、沙漠、地宫各10张；使用全局连续编号，不得因分组重启；分波校验直至每个独立方向至少一个代表获得批准",
    ).replace(
        "【共享视觉胶囊】",
        "【参考图职责】\n参考图1只控制材质完成度和光照质量；构图、建筑、人物、地形和色彩保持中性。\n\n【共享视觉胶囊】",
    ).replace(
        "参考图编号与职责：无。",
        "参考图编号与职责：参考图1只控制材质完成度和光照质量。",
    ).replace(
        "下次必须重新上传的参考图或已批准成片：首次生成后上传所有已批准校验图；当前无已批准成片。",
        "下次必须重新上传的参考图或已批准成片：必须重新上传参考图1；当前无已批准成片。",
    ).replace("计划总数180。", "计划总数60。")
    cases.append(("valid user-grouped quality-reference program", True, fixed_route, fixed_prompt))

    long_capsule = VALID_PROMPT.replace(
        "高端写实CG环境成片，以物理可信的几何、材质响应、自然全局光照、分层空气透视和清晰焦点层级表现巨大而可探索的原创世界。",
        "高端写实CG环境成片。" * 100,
    )
    cases.append(("oversized visual capsule is blocked", False, BASE_ROUTE, long_capsule))

    too_many_refs = copy.deepcopy(BASE_ROUTE)
    too_many_refs["reference_roles"] = [
        {
            "id": f"参考图{i}",
            "role": "environment",
            "capability_class": "general",
            "allow": ["环境"],
            "keep_neutral": ["人物"],
        }
        for i in range(1, 16)
    ]
    cases.append(("dated total reference ceiling is enforced", False, too_many_refs, None))

    multi_role_ref = copy.deepcopy(BASE_ROUTE)
    multi_role_ref["reference_roles"] = [
        {
            "id": "参考图1",
            "role": "material",
            "capability_class": "high-fidelity-object",
            "allow": ["石材响应"],
            "keep_neutral": ["构图", "人物"],
        },
        {
            "id": "参考图1",
            "role": "quality-finish",
            "capability_class": "high-fidelity-object",
            "allow": ["完成度"],
            "keep_neutral": ["构图", "人物"],
        },
    ]
    cases.append(("explicit multiple roles on one reference are valid", True, multi_role_ref, None))

    too_many_objects = copy.deepcopy(BASE_ROUTE)
    too_many_objects["reference_roles"] = [
        {
            "id": f"物体参考{i}",
            "role": "material",
            "capability_class": "high-fidelity-object",
            "allow": ["物体材质"],
            "keep_neutral": ["环境", "人物"],
        }
        for i in range(1, 8)
    ]
    cases.append(("high-fidelity object reference ceiling is enforced", False, too_many_objects, None))

    extend_without_source = copy.deepcopy(BASE_ROUTE)
    extend_without_source.update({"route": "extend", "continuation_source": "", "continuity_reason": "extend-required"})
    cases.append(("extend requires continuity source", False, extend_without_source, None))

    two_output_pause = copy.deepcopy(BASE_ROUTE)
    two_output_pause.update({"complexity": "controlled", "deliverable_count": 2, "pause_mode": "dynamic-verification"})
    cases.append(("two outputs do not create empty verification pause", False, two_output_pause, None))

    omitted_program_pack = copy.deepcopy(BASE_ROUTE)
    omitted_program_pack.update({"continuity_pack": False, "continuity_reason": "one-shot-not-useful"})
    cases.append(("program continuity cannot be silently omitted", False, omitted_program_pack, None))

    results = [expect(*case) for case in cases]
    for _, message in results:
        print(message)
    passed = sum(1 for ok, _ in results if ok)
    print(f"SUMMARY: {passed}/{len(results)} regression cases passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
