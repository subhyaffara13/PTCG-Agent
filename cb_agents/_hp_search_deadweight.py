import logging
from cb_agents.card_registry import CardRegistry

logger = logging.getLogger(__name__)
_registry = CardRegistry()

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
