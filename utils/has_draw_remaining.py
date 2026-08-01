
def has_draw_remaining(candidates: List[str]) -> bool:
    for cand in candidates:
        try:
            if cand.startswith("play_trainer:"):
                name = cand.split(":", 1)[1].lower()
                if any(dk in name for dk in {"research", "iono", "judge", "concealed cards",
                                              "flower selecting", "shining arcana", "colress"}):
                    return True
            if cand.startswith("ability:"):
                target = cand.split(":", 1)[1].lower()
                if any(dk in target for dk in _ABILITY_DRAW_KEYWORDS):
                    return True
        except IndexError:
            continue
    return False


def has_draw_remaining(candidates: List[str]) -> bool:
    for cand in candidates:
        try:
            if cand.startswith("play_trainer:"):
                name = cand.split(":", 1)[1].lower()
                if any(dk in name for dk in {"research", "iono", "judge", "concealed cards",
                                              "flower selecting", "shining arcana", "colress"}):
                    return True
            if cand.startswith("ability:"):
                target = cand.split(":", 1)[1].lower()
                if any(dk in target for dk in _ABILITY_DRAW_KEYWORDS):
                    return True
        except IndexError:
            continue
    return False


def has_draw_remaining(candidates: List[str]) -> bool:
    for cand in candidates:
        try:
            if cand.startswith("play_trainer:"):
                name = cand.split(":", 1)[1].lower()
                if any(dk in name for dk in {"research", "iono", "judge", "concealed cards",
                                              "flower selecting", "shining arcana", "colress"}):
                    return True
            if cand.startswith("ability:"):
                target = cand.split(":", 1)[1].lower()
                if any(dk in target for dk in _ABILITY_DRAW_KEYWORDS):
                    return True
        except IndexError:
            continue
    return False

