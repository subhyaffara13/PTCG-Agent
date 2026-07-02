import pulp
from collections import Counter
from scratch.deck_synergy_graph import get_global_synergy_graph
from scratch.deck_setup import EmpiricalCore
def optimize_deck_milp(empirical_core, pool_cards, details, scores, target_size=60):
    """
    Uses Mixed-Integer Linear Programming to perfectly fill the remaining flex slots 
    around the empirical_core to maximize synergy scores while strictly satisfying 
    hypergeometric bounds (e.g. >=12 Basics, >=10 Energies, max 4 of any non-basic energy).
    """
    prob = pulp.LpProblem("DeckOptimization", pulp.LpMaximize)

    is_core_obj = isinstance(empirical_core, EmpiricalCore)
    if is_core_obj:
        core_counts = {str(k): v for k, v in empirical_core.locked_cards.items()}
        flex_pool_ids = {str(k) for k in empirical_core.flex_pool}
    else:
        core_counts = Counter(str(c["card_id"]) for c in empirical_core)
        flex_pool_ids = {str(c["card_id"]) for c in pool_cards}

    graph = get_global_synergy_graph()
    locked_cids = list(core_counts.keys())
    
    card_vars = {}
    for c in pool_cards:
        cid = str(c["card_id"])
        
        if is_core_obj and cid not in core_counts and cid not in flex_pool_ids:
            continue
            
        if cid not in card_vars:
            limit = 60 if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "") else 4
            min_val = core_counts.get(cid, 0)
            if not is_core_obj:
                min_val = min(limit, min_val)
            
            if is_core_obj and cid in core_counts:
                card_vars[cid] = pulp.LpVariable(f"x_{cid}", lowBound=min_val, upBound=min_val, cat='Integer')
            else:
                card_vars[cid] = pulp.LpVariable(f"x_{cid}", lowBound=min_val, upBound=max(limit, min_val), cat='Integer')

    objective_terms = []
    for cid, var in card_vars.items():
        base_score = scores.get(cid, 0)
        synergy_bonus = 0.0
        if locked_cids:
            pmi_sum = sum(graph.get_pmi(int(cid), int(l_cid)) for l_cid in locked_cids)
            synergy_bonus = pmi_sum / len(locked_cids)
        # Using lambda=0.4 as defined in config for PMI weight roughly, or just 0.5
        objective_terms.append((base_score + 0.4 * synergy_bonus) * var)

    prob += pulp.lpSum(objective_terms), "TotalScore"

    prob += pulp.lpSum(card_vars.values()) == target_size, "TotalCards"

    basics = [str(c["card_id"]) for c in pool_cards if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    prob += pulp.lpSum([card_vars[cid] for cid in set(basics) if cid in card_vars]) >= 12, "MinBasics"

    energies = [str(c["card_id"]) for c in pool_cards if c.get("card_type") == "Energy"]
    prob += pulp.lpSum([card_vars[cid] for cid in set(energies) if cid in card_vars]) >= 10, "MinEnergies"
    prob += pulp.lpSum([card_vars[cid] for cid in set(energies) if cid in card_vars]) <= 16, "MaxEnergies"

    trainers = [str(c["card_id"]) for c in pool_cards if c.get("card_type") == "Trainer"]
    prob += pulp.lpSum([card_vars[cid] for cid in set(trainers) if cid in card_vars]) >= 25, "MinTrainers"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if prob.status != pulp.LpStatusOptimal:
        if is_core_obj:
            # Fallback: just return the locked cards
            optimized_deck = []
            id_map = {str(c["card_id"]): c for c in pool_cards}
            for cid, count in core_counts.items():
                if cid in id_map:
                    optimized_deck.extend([id_map[cid]] * count)
            return optimized_deck
        return empirical_core

    optimized_deck = []
    id_map = {str(c["card_id"]): c for c in pool_cards}
    for cid, var in card_vars.items():
        count = int(var.varValue or 0)
        if count > 0:
            optimized_deck.extend([id_map[cid]] * count)

    return optimized_deck
