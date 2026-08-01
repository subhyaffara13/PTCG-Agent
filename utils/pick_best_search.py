from typing import Optional

_SEARCH_KEYWORDS = {"secret box", "ultra", "nest", "vip", "search", "ball", "poffin"}

def pick_best_search(candidates: list) -> Optional[str]:
    best, bs = None, -1
    for cand in candidates:
        if cand.startswith("play_trainer:"):
            target = cand.split(":", 1)[1].lower()
            if any(sk in target for sk in _SEARCH_KEYWORDS):
                score = 4 if "secret box" in target else (3 if "ultra" in target else (2 if "nest" in target else 1))
                if score > bs: bs, best = score, cand
    return best
