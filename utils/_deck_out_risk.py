
def _deck_out_risk(deck: list, counts: dict) -> float:
    draw_count = 0
    for c in deck:
        name = str(c.get("card_name", "")).lower()
        if any(ds in name for ds in _DRAW_SUPPORTER_NAMES):
            draw_count += 1

    est_draw_total = draw_count * 6.5
    est_natural = 12.0
    est_cards_drawn = est_draw_total + est_natural
    penalty = 0.0
    if est_cards_drawn > 50:
        penalty += 0.10
    if est_cards_drawn > 55:
        penalty += 0.15
    if est_cards_drawn > 60:
        penalty += 0.25
    if draw_count >= 8:
        penalty += 0.10
    if draw_count >= 12:
        penalty += 0.25
    return min(penalty, 0.6)

