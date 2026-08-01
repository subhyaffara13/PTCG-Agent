
def _score_deck_out(v: float, action: str, gs: dict, dc: int, opp_dc: int, opp_hp: float) -> float:
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    if dc <= 8 and opp_hp > 0:
        if action.startswith("play_trainer:"):
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"research", "professor", "carmine", "lillie", "iono", "judge"}):
                v -= 1.0
        elif action.startswith("ability:"):
            tn = action.split(":", 1)[1].lower()
            if any(d in tn for d in {"colress", "concealed", "draw"}):
                v -= 1.0
    if hs >= 2 and dc > 10:
        v += 0.03 * min(hs, 5)
    _avg_draw = 1.5
    my_turns_left = dc / _avg_draw if dc > 0 else 0
    opp_turns_left = opp_dc / _avg_draw if opp_dc > 0 else 0
    we_outlast = my_turns_left > opp_turns_left + 1
    if action.startswith("play_trainer:"):
        tn = action.split(":", 1)[1].lower()
        is_shuffle = any(k in tn for k in {"iono", "judge"})
        is_draw = any(k in tn for k in {"research", "professor", "carmine", "lillie"})
        if (opp_dc < dc or (opp_dc < 10 and we_outlast)) and is_shuffle:
            v += 1.2
        elif opp_dc < 8 and we_outlast:
            if is_draw:
                v -= 0.8
            if "pass" in action or any(k in tn for k in {"potion", "heal", "switch", "scoop"}):
                v += 0.6
    elif action in ("pass",) and opp_dc < 10 and we_outlast:
        v += 0.8
    elif action.startswith("retreat:") and opp_dc < 10 and we_outlast:
        v += 0.4
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        if opp_dc < 10 and we_outlast and any(d in tn for d in {"heal", "protect", "barrier"}):
            v += 0.5
    return v


def _score_deck_out(v: float, action: str, gs: dict, dc: int, opp_dc: int, opp_hp: float) -> float:
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    if dc <= 8 and opp_hp > 0:
        if action.startswith("play_trainer:"):
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"research", "professor", "carmine", "lillie", "iono", "judge"}):
                v -= 1.0
        elif action.startswith("ability:"):
            tn = action.split(":", 1)[1].lower()
            if any(d in tn for d in {"colress", "concealed", "draw"}):
                v -= 1.0
    if hs >= 2 and dc > 10:
        v += 0.03 * min(hs, 5)
    _avg_draw = 1.5
    my_turns_left = dc / _avg_draw if dc > 0 else 0
    opp_turns_left = opp_dc / _avg_draw if opp_dc > 0 else 0
    we_outlast = my_turns_left > opp_turns_left + 1
    if action.startswith("play_trainer:"):
        tn = action.split(":", 1)[1].lower()
        is_shuffle = any(k in tn for k in {"iono", "judge"})
        is_draw = any(k in tn for k in {"research", "professor", "carmine", "lillie"})
        if (opp_dc < dc or (opp_dc < 10 and we_outlast)) and is_shuffle:
            v += 1.2
        elif opp_dc < 8 and we_outlast:
            if is_draw:
                v -= 0.8
            if "pass" in action or any(k in tn for k in {"potion", "heal", "switch", "scoop"}):
                v += 0.6
    elif action in ("pass",) and opp_dc < 10 and we_outlast:
        v += 0.8
    elif action.startswith("retreat:") and opp_dc < 10 and we_outlast:
        v += 0.4
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        if opp_dc < 10 and we_outlast and any(d in tn for d in {"heal", "protect", "barrier"}):
            v += 0.5
    return v

