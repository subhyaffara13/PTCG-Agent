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
        from agents.strategy_agent_io import load_skill
        self._profiles: dict[str, dict[str, Any]] = load_skill(kwargs.get("skills_dir"))

    def evaluate(self, packet: dict[str, Any]) -> dict[str, Any]:
        if hasattr(packet, "model_dump"): packet = packet.model_dump()
        elif hasattr(packet, "_asdict"): packet = packet._asdict()
        elif hasattr(packet, "__dict__"): packet = packet.__dict__
        trigger: str = str(packet.get("trigger", "")).strip()
        board_summary: dict = packet.get("board_summary", {})
        profile_key, profile, confidence, match_reason = self._match_profile(
            trigger, board_summary
        )
        result: dict[str, Any] = {
            "strategy":   profile_key,
            "posture":    profile.get("posture", "tempo"),
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
        
        board_match = self._board_signal_match(board_summary)
        if board_match:
            key = board_match
            if key not in self._profiles:
                raise ValueError(f"CRITICAL SILENT FAILURE PREVENTED: Strategy key '{key}' is missing from strategy_profiles.json!")
            return key, self._profiles[key], _CONF_KEYWORD, f"board_summary signal -> {key}"
            
        best_key, best_score = self._keyword_scan(trigger_lower)
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

    def _board_signal_match(self, board_summary: dict[str, Any]) -> str | None:
        prizes     = board_summary.get("prizes")
        bench      = board_summary.get("bench_count")
        score      = board_summary.get("hand_score")
        energy     = board_summary.get("energy_attached")
        opp_prizes = board_summary.get("opponent_prizes")
        
        boss_prob  = board_summary.get("boss_prob", 0.0)
        iono_prob  = board_summary.get("iono_prob", 0.0)

        if boss_prob > 0.7 and bench is not None and int(bench) > 0:
            return "stall"

        if iono_prob > 0.7 and score is not None and float(score) > 5.0:
            return "aggro_push"

        if prizes is not None and int(prizes) <= 2:
            return "endgame_close"
        if opp_prizes is not None and int(opp_prizes) <= 2:
            return "prize_race"
        if bench is not None and int(bench) <= 1:
            return "bench_low"
        if energy is not None and int(energy) == 0:
            return "energy_stall"
        if score is not None and float(score) < 2.0:
            return "hand_dead"
            
        p_val = int(prizes) if prizes is not None else 6
        if p_val >= 5: return "setup"
        if p_val >= 3: return "aggro"
        return "endgame_close"

    def _keyword_scan(self, trigger_lower: str) -> tuple[str | None, float]:
        best_key, best_score = None, 0.0
        for key, profile in self._profiles.items():
            trigger_desc = profile.get("trigger", "").lower()
            words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
            if not words:
                continue
            matched = sum(1 for w in words if w in trigger_lower)
            score   = matched / len(words)
            if score > best_score:
                best_score, best_key = score, key
        return best_key, best_score

    def _log(
        self,
        packet: dict[str, Any],
        matched_key: str,
        match_reason: str,
        result: dict[str, Any],
    ) -> None:
        from agents.strategy_agent_io import log_strategy
        log_strategy(packet, matched_key, match_reason, result, list(self._profiles.keys()))
