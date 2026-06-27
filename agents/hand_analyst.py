from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "card_scoring.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"

_PROFILE_THRESHOLDS: list[tuple[float, str]] = [
    (7.0, "aggressive"),
    (4.0, "tempo"),
    (0.0, "defensive"),
]


class HandAnalyst:
    def __init__(self) -> None:
        self._scoring_db: dict[str, dict[str, Any]] = self._load_skill()
        self._log_buffer: list[dict[str, Any]] = []

    def flush_logs(self) -> None:
        if not self._log_buffer:
            return
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.extend(self._log_buffer)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
        self._log_buffer.clear()

    def analyse(self, packet: dict[str, Any]) -> dict[str, Any]:
        hand: list[str]    = packet["hand"]
        deck_remaining: int = packet.get("deck_remaining", 0)
        scored_cards        = self._score_hand(hand)
        hand_score          = self._mean_ev(scored_cards)
        priority_profile    = self._derive_profile(hand_score)
        top_play            = self._best_card(scored_cards)
        result = {
            "hand_score":       round(hand_score, 4),
            "priority_profile": priority_profile,
            "top_play":         top_play,
        }
        self._log(hand, deck_remaining, scored_cards, result)
        return result

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw   = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        index = {}
        for entry in raw.get("cards", []):
            name = entry.get("card_name", "").strip()
            if name:
                index[name] = entry
        return index

    def _score_hand(self, hand: list[str]) -> list[tuple[str, float]]:
        scored = []
        for card_name in hand:
            entry    = self._scoring_db.get(card_name, {})
            ev_score = float(entry.get("ev_score", 0.0))
            scored.append((card_name, ev_score))
        return scored

    def _mean_ev(self, scored_cards: list[tuple[str, float]]) -> float:
        if not scored_cards:
            return 0.0
        return sum(ev for _, ev in scored_cards) / len(scored_cards)

    def _derive_profile(self, hand_score: float) -> str:
        for threshold, profile in _PROFILE_THRESHOLDS:
            if hand_score >= threshold:
                return profile
        return "defensive"

    def _best_card(self, scored_cards: list[tuple[str, float]]) -> str:
        if not scored_cards:
            return "(empty hand)"
        return max(scored_cards, key=lambda t: t[1])[0]

    def _log(self, hand, deck_remaining, scored_cards, result):
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "HandAnalyst",
            "input":     {"hand": hand, "deck_remaining": deck_remaining},
            "reasoning": {
                "card_scores":   [{"card": n, "ev_score": e} for n, e in scored_cards],
                "unknown_cards": [n for n, e in scored_cards if e == 0.0],
            },
            "output": result,
        }
        self._log_buffer.append(entry)
