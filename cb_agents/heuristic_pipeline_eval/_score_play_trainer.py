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
    if hs > 5 and dc > 10:
        if any(k in tn for k in {"iono", "judge"}):
            v += min(0.6, hs * 0.08)
        if any(k in tn for k in {"research", "professor", "carmine"}):
            v += min(0.4, hs * 0.05)
    return v
