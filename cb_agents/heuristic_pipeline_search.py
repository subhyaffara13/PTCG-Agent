"""
Sub-module: thinning_value, pick_best_search, dead_weight
"""

import logging
from typing import Optional
from cb_agents.card_registry import CardRegistry

logger = logging.getLogger(__name__)
_registry = CardRegistry()

_SEARCH_KEYWORDS = {"ultra", "nest", "level", "heavy", "quick", "pokeball", "signal", "secret box", "petrel", "earthen vessel"}


def thinning_value(candidate: str, game_state: dict) -> float:
    if not candidate.startswith("play_trainer:"): return 0.0
    name = candidate.split(":", 1)[1].lower()
    if not any(sk in name for sk in _SEARCH_KEYWORDS): return 0.0
    dc = game_state.get("my_deck_count", 60)
    return 0.3 if dc > 45 else (0.15 if dc > 30 else 0.0)


def pick_best_search(candidates: list) -> Optional[str]:
    best, bs = None, -1
    for cand in candidates:
        if cand.startswith("play_trainer:"):
            target = cand.split(":", 1)[1].lower()
            if any(sk in target for sk in _SEARCH_KEYWORDS):
                score = 4 if "secret box" in target else (3 if "ultra" in target else (2 if "nest" in target else 1))
                if score > bs: bs, best = score, cand
    return best


def dead_weight(candidates: list, gs: dict) -> bool:
    try:
        hand = gs.get("my_hand", [])
        if not isinstance(hand, list) or len(hand) < 4: return False
        unplayable = 0
        total_supporters = 0
        basic_energy_count = 0
        total_search = 0
        deck_count = gs.get("my_deck_count", 60)
        for cid in hand:
            try:
                c = _registry.get(int(cid))
                if not c: continue
                ct = c.card_type.name
                if ct == "TRAINER" and getattr(c, "trainer_subtype", None) and c.trainer_subtype.name == "SUPPORTER":
                    total_supporters += 1
                elif c.stage and c.stage.name == "STAGE2":
                    unplayable += 1
                elif ct == "TRAINER" and getattr(c, "trainer_subtype", None) and c.trainer_subtype.name == "ITEM":
                    name_lower = c.card_name.lower()
                    if any(sk in name_lower for sk in ("ultra ball", "dusk ball", "pokegear", "energy search")):
                        total_search += 1
                elif ct == "ENERGY":
                    basic_energy_count += 1
            except Exception as e:
                logger.debug(f"Card check failed in dead_weight analysis for {cid}: {e}")
        if total_supporters > 1:
            unplayable += (total_supporters - 1)
        if basic_energy_count >= 5:
            unplayable += (basic_energy_count - 4)
        if total_search >= 2 and deck_count <= 20:
            unplayable += total_search
        return unplayable >= 4
    except Exception as e:
        logger.error(f"dead_weight failed: {e}"); return False
