"""Board-strategy selection agent. Delegates I/O to strategy_agent_io."""

from __future__ import annotations
from typing import Any

_CONF_EXACT_KEY = 1.0
_CONF_KEYWORD = 0.75
_CONF_FALLBACK = 0.3
_FALLBACK_PROFILE_KEY = "hand_dead"


class StrategyAgent:
    """Selects the best strategic posture for the current board state."""

    def __init__(self, **kwargs: Any) -> None:
        from cb_agents.strategy_agent_io import load_skill
        self.current_posture = "tempo"
        self.last_triggered_turn = 0
        try:
            self._profiles: dict[str, dict[str, Any]] = load_skill(kwargs.get("skills_dir"))
        except Exception as e:
            self._profiles = {}

    def evaluate(self, packet: Any) -> dict[str, Any]:
        try:
            return self._evaluate_internal(packet)
        except Exception as e:
            return {
                "strategy": "error_fallback",
                "posture": "tempo",
                "actions": ["PASS"],
                "escalation": "PASS",
                "confidence": 0.0,
            }

    def _evaluate_internal(self, packet: dict[str, Any]) -> dict[str, Any]:
        if hasattr(packet, "model_dump"): packet = packet.model_dump()
        elif hasattr(packet, "_asdict"): packet = packet._asdict()
        elif hasattr(packet, "__dict__"): packet = packet.__dict__
        if not isinstance(packet, dict):
            packet = {}
        trigger: str = str(packet.get("trigger", "")).strip()
        board_summary: dict = packet.get("board_summary", {})
        
        # Turn 1 Bad Deck Early Warning System
        if board_summary.get("turn_number", packet.get("turn", 0)) == 1 and not hasattr(self, "_checked_deck"):
            self._checked_deck = True
            deck = packet.get("deck", []) or board_summary.get("deck", [])
            if deck:
                from cb_agents.turn_planner_heuristics import _registry
                elements = set()
                basics = 0
                for cid in deck:
                    c = _registry.get(int(cid) if str(cid).isdigit() else cid)
                    if c and c.card_type.name == "POKEMON":
                        # Simulate stage check, but simpler for now:
                        basics += 1
                        # Wait, CardEntry doesn't have element_type directly. We will pull it from registry full skill.
                        try:
                            full = _registry.get_full_skill(int(cid))
                            if full and hasattr(full, "element_type"):
                                elements.add(full.element_type)
                        except Exception:
                            pass
                if len(elements) >= 4 or (len(deck) > 20 and basics < 3):
                    import logging
                    logging.getLogger("StrategyAgent").error(f"CRITICAL WARNING: Executing with a highly unoptimized/brick-risk deck! Detected {len(elements)} elemental types.")
                    print(f"CRITICAL WARNING: Executing with a highly unoptimized/brick-risk deck! Detected {len(elements)} elemental types.")

        profile_key, profile, confidence, match_reason = self._match_profile(
            trigger, board_summary
        )
        posture_val = profile.get("posture", "tempo")
        self.current_posture = posture_val
        turn_num = board_summary.get("turn_number", packet.get("turn", 1))
        if trigger.lower() != "none":
            self.last_triggered_turn = turn_num
            
        result: dict[str, Any] = {
            "strategy":   profile_key,
            "posture":    posture_val,
            "actions":    profile.get("actions", ["PASS"]),
            "escalation": profile.get("escalation", "PASS"),
            "confidence": round(confidence, 4),
        }
        self._log(packet, profile_key, match_reason, result)
        return result

    receive = evaluate

    def _match_profile(
        self,
        trigger: str,
        board_summary: dict[str, Any],
    ) -> tuple[str, dict[str, Any], float, str]:
        trigger_lower = trigger.lower()
        if trigger_lower in self._profiles:
            return trigger_lower, self._profiles[trigger_lower], _CONF_EXACT_KEY, "exact key match"
        
        from cb_agents.strategy_agent_io import board_signal_match, keyword_scan
        board_match = board_signal_match(board_summary)
        if board_match:
            key = board_match
            if key not in self._profiles:
                raise ValueError(f"CRITICAL SILENT FAILURE PREVENTED: Strategy key '{key}' is missing from strategy_profiles.json!")
            return key, self._profiles[key], _CONF_KEYWORD, f"board_summary signal -> {key}"
            
        best_key, best_score = keyword_scan(trigger_lower, self._profiles)
        if best_key and best_score > 0:
            return (
                best_key,
                self._profiles[best_key],
                _CONF_KEYWORD * best_score,
                f"keyword scan score={best_score:.2f}",
            )
            
        if _FALLBACK_PROFILE_KEY not in self._profiles:
            raise ValueError(f"CRITICAL SILENT FAILURE PREVENTED: Fallback key '{_FALLBACK_PROFILE_KEY}' is missing from strategy_profiles.json!")
        fallback = self._profiles[_FALLBACK_PROFILE_KEY]
        return _FALLBACK_PROFILE_KEY, fallback, _CONF_FALLBACK, "no match -> fallback"

    def _log(
        self,
        packet: dict[str, Any],
        matched_key: str,
        match_reason: str,
        result: dict[str, Any],
    ) -> None:
        from cb_agents.strategy_agent_io import log_strategy
        log_strategy(packet, matched_key, match_reason, result, list(self._profiles.keys()))
