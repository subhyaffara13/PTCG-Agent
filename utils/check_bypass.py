from typing import Optional

def check_bypass(pipeline, candidates: list, gs: dict, rules: dict) -> Optional[str]:
    try:
        dc = gs.get("my_deck_count", 60)
        hand = gs.get("my_hand", [])
        hd = pipeline.dead_weight(candidates, gs)
        hs = "strong" if isinstance(hand, list) and len(hand) >= 7 else ("medium" if isinstance(hand, list) and len(hand) >= 4 else "weak")
        if hs == "weak" and dc > 8:
            bench = gs.get("my_bench", [])
            has_basic_in_hand = False
            if isinstance(hand, list):
                from cb_agents.card_registry import CardRegistry
                reg = CardRegistry()
                for cid in hand:
                    try:
                        c = reg.get(int(cid))
                        if c and c.stage and c.stage.name == "BASIC":
                            has_basic_in_hand = True
                            break
                    except Exception:
                        pass
            if len(bench) == 0 and not has_basic_in_hand:
                bs = pipeline.pick_best_search(candidates)
                if bs: logger.debug(f"Bypass: {bs} (dead hand, no bench)"); return bs
                for ca in candidates:
                    if ca.startswith("ability:"):
                        t = ca.split(":", 1)[1].lower()
                        if any(d in t for d in ABILITY_DRAW):
                            logger.debug(f"Bypass: {ca} (ability - dead hand)"); return ca
                for ca in candidates:
                    if ca.startswith("play_trainer:"):
                        t = ca.split(":", 1)[1].lower()
                        if any(d in t for d in DRAW_SUPPORTERS):
                            logger.debug(f"Bypass: {ca} (supporter - dead hand)"); return ca
        elif hd and dc > 8:
            bs = pipeline.pick_best_search(candidates)
            if bs: logger.debug(f"Bypass: {bs} (dead weight={hd})"); return bs
    except Exception as e:
        logger.error(f"check_bypass failed: {e}", exc_info=True)
    return None


def check_bypass(pipeline, candidates: list, gs: dict, rules: dict) -> Optional[str]:
    try:
        dc = gs.get("my_deck_count", 60)
        hand = gs.get("my_hand", [])
        hd = pipeline.dead_weight(candidates, gs)
        hs = "strong" if isinstance(hand, list) and len(hand) >= 7 else ("medium" if isinstance(hand, list) and len(hand) >= 4 else "weak")
        if hs == "weak" and dc > 8:
            bench = gs.get("my_bench", [])
            has_basic_in_hand = False
            if isinstance(hand, list):
                from cb_agents.card_registry import CardRegistry
                reg = CardRegistry()
                for cid in hand:
                    try:
                        c = reg.get(int(cid))
                        if c and c.stage and c.stage.name == "BASIC":
                            has_basic_in_hand = True
                            break
                    except Exception:
                        pass
            if len(bench) == 0 and not has_basic_in_hand:
                bs = pipeline.pick_best_search(candidates)
                if bs: logger.debug(f"Bypass: {bs} (dead hand, no bench)"); return bs
                for ca in candidates:
                    if ca.startswith("ability:"):
                        t = ca.split(":", 1)[1].lower()
                        if any(d in t for d in ABILITY_DRAW):
                            logger.debug(f"Bypass: {ca} (ability - dead hand)"); return ca
                for ca in candidates:
                    if ca.startswith("play_trainer:"):
                        t = ca.split(":", 1)[1].lower()
                        if any(d in t for d in DRAW_SUPPORTERS):
                            logger.debug(f"Bypass: {ca} (supporter - dead hand)"); return ca
        elif hd and dc > 8:
            bs = pipeline.pick_best_search(candidates)
            if bs: logger.debug(f"Bypass: {bs} (dead weight={hd})"); return bs
    except Exception as e:
        logger.error(f"check_bypass failed: {e}", exc_info=True)
    return None

