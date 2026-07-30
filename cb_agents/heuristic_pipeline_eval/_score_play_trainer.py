def _score_play_trainer(v: float, action: str, gs: dict, dc: int, opp_dc: int) -> float:
    if not action.startswith("play_trainer:"):
        return v
    v += 0.4
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    tn = action.split(":", 1)[1].lower()
    if dc <= 3:
        if any(k in tn for k in {"iono", "judge", "research", "professor", "carmine", "lillie", "colress"}):
            v -= 10.0
    elif dc <= 5:
        if any(k in tn for k in {"research", "professor", "carmine", "lillie", "colress"}):
            v -= 5.0
        elif any(k in tn for k in {"iono", "judge"}):
            v -= 3.0
    elif dc <= 7:
        if any(k in tn for k in {"iono", "judge"}):
            v -= 2.5
        elif any(k in tn for k in {"research", "professor", "carmine", "lillie", "colress"}):
            v -= 2.5
    if dc > 30:
        sk = {"nest ball", "ultra ball", "quick ball", "level ball", "secret box", "mega signal", "team rocket's petrel"}
        if any(s in tn for s in sk):
            v += min(0.25, dc * 0.005)
    my_prizes = gs.get("my_prizes", 6)
    opp_prizes = gs.get("opponent_prizes", 6)
    opp_hand = gs.get("opponent_hand_count", 5)

    if "iono" in tn:
        # Prize-aware Iono disruption evaluation
        if opp_prizes <= 2 and opp_hand >= 3:
            v += 1.5  # Critical late-game disruption: forces opponent down to 1-2 cards
        elif opp_prizes <= 3 and opp_hand >= 4:
            v += 0.8
        if my_prizes <= 2 and hs >= 4:
            v -= 1.0  # Self-disruption penalty: avoid reducing own 4+ card hand to 1-2 cards
    elif "judge" in tn:
        if opp_hand >= 5:
            v += 0.5  # Disrupt opponent's large hand
        if hs < 4 and dc > 10:
            v += 0.3  # Draw up to 4 when our hand is low
    elif any(k in tn for k in {"research", "professor", "carmine"}):
        if hs > 5 and dc > 10:
            v += min(0.4, hs * 0.05)
    return v
