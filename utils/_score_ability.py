
def _score_ability(v: float, action: str, dc: int, opp_dc: int) -> float:
    if not action.startswith("ability:"):
        return v
    tn = action.split(":", 1)[1].lower()
    v += 0.35
    if dc <= 7 and any(d in tn for d in {"colress", "concealed", "draw"}):
        v -= 2.0
    elif dc <= 20 and dc < opp_dc - 3 and any(d in tn for d in {"colress", "concealed", "draw"}):
        v -= 0.8
    return v


def _score_ability(v: float, action: str, dc: int, opp_dc: int) -> float:
    if not action.startswith("ability:"):
        return v
    tn = action.split(":", 1)[1].lower()
    v += 0.35
    if dc <= 7 and any(d in tn for d in {"colress", "concealed", "draw"}):
        v -= 2.0
    elif dc <= 20 and dc < opp_dc - 3 and any(d in tn for d in {"colress", "concealed", "draw"}):
        v -= 0.8
    return v

