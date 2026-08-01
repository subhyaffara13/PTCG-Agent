
def _draw_supporter_penalty(deck, cs):
    draw_supporters_count = sum(1 for c in deck if c.card_type == "Trainer" and
        any(k in c.card_name.lower() for k in {"research", "lillie", "carmine", "professor"}))
    has_recovery = any("pad" in c.card_name.lower() or "stretcher" in c.card_name.lower() or
        "rod" in c.card_name.lower() for c in deck)
    if draw_supporters_count >= 4 and not has_recovery:
        cs = max(0.0, cs - 0.2)
    return cs

