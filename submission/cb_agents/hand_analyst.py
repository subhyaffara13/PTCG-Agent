from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any
from cb_agents.log_flusher import flush_reasoning_logs
import logging

logger = logging.getLogger(__name__)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "card_scoring.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"

_PROFILE_THRESHOLDS: list[tuple[float, str]] = [
    (7.0, "aggressive"),
    (4.0, "tempo"),
    (0.0, "defensive"),
]


class HandAnalyst:
    def __init__(self, **kwargs: Any) -> None:
        self.skills_dir = pathlib.Path(kwargs.get("skills_dir")) if kwargs.get("skills_dir") else _PROJECT_ROOT / "skills"
        self.log_dir = pathlib.Path(kwargs.get("log_dir")) if kwargs.get("log_dir") else _PROJECT_ROOT / "logs"
        self._scoring_db: dict[str, dict[str, Any]] = self._load_skill()
        self._log_buffer: list[dict[str, Any]] = []

    def flush_logs(self) -> None:
        log_path = self.log_dir / "reasoning_log.json"
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        flush_reasoning_logs(self._log_buffer, log_path, logger)

    def analyse(self, packet: dict[str, Any]) -> dict[str, Any]:
        if hasattr(packet, "model_dump"): packet = packet.model_dump()
        elif hasattr(packet, "_asdict"): packet = packet._asdict()
        elif hasattr(packet, "__dict__"): packet = packet.__dict__
        hand: list[str]    = packet["hand"]
        deck_remaining: int = packet.get("deck_remaining", 0)
        scored_cards        = self._score_hand(hand)
        hand_score          = self._mean_ev(scored_cards)
        self.last_hand_score = hand_score
        priority_profile    = self._derive_profile(hand_score)
        top_play            = self._best_card(scored_cards)
        result = {
            "hand_score":       round(hand_score, 4),
            "priority_profile": priority_profile,
            "top_play":         top_play,
        }
        self._log(hand, deck_remaining, scored_cards, result)
        return result

    receive = analyse

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        skill_path = self.skills_dir / "card_scoring.json"
        try:
            raw = json.loads(skill_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raw = {"cards": []}
        index = {}
        for entry in raw.get("cards", []):
            name = entry.get("card_name", "").strip()
            if name:
                index[name.lower()] = entry
        return index

    def _score_hand(self, hand: list[str]) -> list[tuple[str, float]]:
        from cb_agents.hand_analyst_helpers import score_hand_helper
        return score_hand_helper(hand, self._scoring_db)

    def _mean_ev(self, scored_cards: list[tuple[str, float]]) -> float:
        from cb_agents.hand_analyst_helpers import mean_ev_helper
        return mean_ev_helper(scored_cards)

    def _derive_profile(self, hand_score: float) -> str:
        from cb_agents.hand_analyst_helpers import derive_profile_helper
        return derive_profile_helper(hand_score, _PROFILE_THRESHOLDS)

    def _best_card(self, scored_cards: list[tuple[str, float]]) -> str:
        from cb_agents.hand_analyst_helpers import best_card_helper
        return best_card_helper(scored_cards)

    def _log(self, hand, deck_remaining, scored_cards, result):
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
            "agent":     "HandAnalyst",
            "input":     {"hand": hand, "deck_remaining": deck_remaining},
            "reasoning": {
                "card_scores":   [{"card": n, "ev_score": e} for n, e in scored_cards],
                "unknown_cards": [n for n, e in scored_cards if e == 0.0],
            },
            "output": result,
        }
        self._log_buffer.append(entry)
