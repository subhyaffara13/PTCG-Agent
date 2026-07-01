import random
from collections import Counter
from scratch.deck_synergy_graph import get_global_synergy_graph
from scratch.deck_setup import EmpiricalCore

def _card_key(deck):
    return tuple(sorted(c["card_id"] for c in deck))

def _card_type_counts(deck, details):
    return (
        sum(1 for c in deck if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"),
        sum(1 for c in deck if c.get("card_type") == "Energy"),
        sum(1 for c in deck if c.get("card_type") == "Trainer"),
    )

def mutate_deck(deck: list, pokemon_pool: list, basics: list, energy_pool: list,
                trainer_pool: dict, pool_cards: list, details: dict, mutation_rate: float = 0.3,
                empirical_core=None) -> list:
    is_core_obj = isinstance(empirical_core, EmpiricalCore)
    if is_core_obj:
        locked_cards = empirical_core.locked_cards
        flex_pool = empirical_core.flex_pool
    else:
        locked_cards = {}
        flex_pool = [int(c["card_id"]) for c in pool_cards]

    graph = get_global_synergy_graph()
    result = list(deck)
    
    deck_cids = [int(c["card_id"]) for c in result]
    locked_counts = Counter(locked_cards)
    
    flex_indices = []
    assigned_locks = Counter()
    for idx, cid in enumerate(deck_cids):
        if assigned_locks[cid] < locked_counts[cid]:
            assigned_locks[cid] += 1
        else:
            flex_indices.append(idx)
            
    id_map = {int(c["card_id"]): c for c in pool_cards}
    
    for idx in flex_indices:
        if random.random() >= mutation_rate:
            continue
            
        c = result[idx]
        ctype = c.get("card_type")
        
        # Count existing cards in the deck excluding the index being mutated
        current_counts = Counter(int(card["card_id"]) for i, card in enumerate(result) if i != idx)
        
        valid_candidates = []
        for cid in flex_pool:
            cand = id_map.get(cid)
            if not cand: continue
            if ctype == cand.get("card_type"):
                cand_id = int(cand["card_id"])
                # Enforce the 4-copy rule unless it is Basic Energy
                is_basic_energy = "ENERGY" in str(cand.get("card_type")).upper() and "BASIC" in str(cand.get("card_name", "")).upper()
                if not is_basic_energy and current_counts[cand_id] >= 4:
                    continue
                valid_candidates.append(cand)
                
        if not valid_candidates:
            continue
            
        if len(valid_candidates) > 30:
            valid_candidates = random.sample(valid_candidates, 30)
            
        weights = []
        for cand in valid_candidates:
            cand_id = int(cand["card_id"])
            pmi_sum = 0.0
            for other_cid in deck_cids:
                if other_cid != cand_id:
                    pmi_sum += graph.get_pmi(cand_id, other_cid)
            w = max(0.1, 1.0 + pmi_sum / max(1, len(deck_cids) - 1))
            weights.append(w)
            
        replacement = random.choices(valid_candidates, weights=weights, k=1)[0]
        result[idx] = replacement
        deck_cids[idx] = int(replacement["card_id"])

    return result
