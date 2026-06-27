# Content for agents/turn_planner.py

TURN_PLANNER = """\
\"\"\"
agents/turn_planner.py
----------------------
Translates a hand summary into an ordered action plan for this turn.

Contract
--------
- Skill file  : skills/priority_rules.json  (loaded once at __init__, never again)
- Input packet: { hand_score: float, priority_profile: str }  -- from Router only
- Output      : list[dict]  -- ordered action plan, highest priority first
- Logs        : every plan + per-decision rationale -> logs/reasoning_log.json
- File access : priority_rules.json and reasoning_log.json ONLY
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT      = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH        = _PROJECT_ROOT / "skills" / "priority_rules.json"
_LOG_PATH          = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_KO_SCORE_THRESHOLD: float = 6.0


class TurnPlanner:
    def __init__(self) -> None:
        self._rules: list[dict[str, Any]]          = []
        self._overrides: dict[str, dict[str, Any]] = {}
        self._load_skill()

    def plan(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
        hand_score: float = float(packet.get("hand_score", 0.0))
        profile:    str   = packet.get("priority_profile", "tempo")
        active_rules      = self._apply_profile(profile)
        action_plan       = self._evaluate_rules(active_rules, hand_score, profile)
        self._log(packet, active_rules, action_plan)
        return action_plan

    def _load_skill(self) -> None:
        raw              = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        self._rules      = sorted(raw.get("rules", []), key=lambda r: r["priority"])
        self._overrides  = raw.get("profile_overrides", {})

    def _apply_profile(self, profile: str) -> list[dict[str, Any]]:
        override   = self._overrides.get(profile, {})
        boosted    = set(override.get("boost",    []))
        suppressed = set(override.get("suppress", []))
        filtered   = [r for r in self._rules if r["action"] not in suppressed]
        return (
            [r for r in filtered if r["action"] in boosted]
            + [r for r in filtered if r["action"] not in boosted]
        )

    def _evaluate_rules(self, rules, hand_score, profile):
        plan: list[dict[str, Any]] = []
        for rule in rules:
            action    = rule["action"]
            rationale = rule["rationale"]
            if action == "PASS":
                continue
            viable, why = self._is_viable(action, hand_score, profile, rationale)
            plan.append({"action": action, "viable": viable, "rationale": why})
        plan.append({"action": "PASS", "viable": True, "rationale": "Fallback: legal in all board states."})
        return plan

    def _is_viable(self, action, hand_score, profile, base_rationale):
        if action == "ATTACK_KO":
            viable = hand_score >= _KO_SCORE_THRESHOLD
            why = (
                f"hand_score {hand_score:.2f} >= KO threshold {_KO_SCORE_THRESHOLD} -> attack likely viable."
                if viable else
                f"hand_score {hand_score:.2f} < KO threshold {_KO_SCORE_THRESHOLD} -> attack unlikely this turn."
            )
            return viable, why
        if action == "EVOLVE":
            viable = profile in ("aggressive", "tempo")
            why = (
                f"Profile '{profile}' typically runs evolution lines."
                if viable else
                f"Profile '{profile}' is defensive; evolution less likely."
            )
            return viable, why
        if action == "ATTACH_ENERGY":
            return True, "Energy attachment is a once-per-turn action; always take it if available."
        if action == "PLAY_TRAINER":
            return True, base_rationale
        return True, f"No heuristic defined for '{action}'. Deferring to Orchestrator."
"""
