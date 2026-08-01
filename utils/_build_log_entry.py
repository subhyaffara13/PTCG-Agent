
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

