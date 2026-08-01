
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

