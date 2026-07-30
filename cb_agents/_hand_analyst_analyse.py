import datetime
from typing import Any

_PROFILE_THRESHOLDS: list[tuple[float, str]] = [
    (7.0, "aggressive"),
    (4.0, "tempo"),
    (0.0, "defensive"),
]

def _score_hand(hand: list[str], _scoring_db: dict) -> list[tuple[str, float]]:
    from cb_agents.hand_analyst_helpers import score_hand_helper
    return score_hand_helper(hand, _scoring_db)

def _mean_ev(scored_cards: list[tuple[str, float]]) -> float:
    from cb_agents.hand_analyst_helpers import mean_ev_helper
    return mean_ev_helper(scored_cards)

def _derive_profile(hand_score: float) -> str:
    from cb_agents.hand_analyst_helpers import derive_profile_helper
    return derive_profile_helper(hand_score, _PROFILE_THRESHOLDS)

def _best_card(scored_cards: list[tuple[str, float]]) -> str:
    from cb_agents.hand_analyst_helpers import best_card_helper
    return best_card_helper(scored_cards)

def _analyse_packet(packet: dict[str, Any], _scoring_db: dict) -> tuple:
    hand: list[str] = packet["hand"]
    scored_cards = _score_hand(hand, _scoring_db)
    hand_score = _mean_ev(scored_cards)
    priority_profile = _derive_profile(hand_score)
    top_play = _best_card(scored_cards)
    result = {
        "hand_score": round(hand_score, 4),
        "priority_profile": priority_profile,
        "top_play": top_play,
    }
    return result, scored_cards

def _build_log_entry(hand, deck_remaining, scored_cards, result):
    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent": "HandAnalyst",
        "input": {"hand": hand, "deck_remaining": deck_remaining},
        "reasoning": {
            "card_scores": [{"card": n, "ev_score": e} for n, e in scored_cards],
            "unknown_cards": [n for n, e in scored_cards if e == 0.0],
        },
        "output": result,
    }
