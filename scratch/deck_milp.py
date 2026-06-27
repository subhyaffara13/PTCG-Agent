import pulp
from collections import Counter
from scratch.deck_simulator import evaluate_deck_synergy

def optimize_deck_milp(empirical_core, pool_cards, details, scores, target_size=60):
    """
    Uses Mixed-Integer Linear Programming to perfectly fill the remaining flex slots 
    around the empirical_core to maximize synergy scores while strictly satisfying 
    hypergeometric bounds (e.g. >=12 Basics, >=10 Energies, max 4 of any non-basic energy).
    """
    prob = pulp.LpProblem("DeckOptimization", pulp.LpMaximize)

    core_counts = Counter(str(c["card_id"]) for c in empirical_core)
    
    card_vars = {}
    for c in pool_cards:
        cid = str(c["card_id"])
        if cid not in card_vars:
            limit = 60 if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "") else 4
            min_val = core_counts.get(cid, 0)
            card_vars[cid] = pulp.LpVariable(f"x_{cid}", lowBound=min_val, upBound=max(limit, min_val), cat='Integer')

    prob += pulp.lpSum([scores.get(cid, 0) * var for cid, var in card_vars.items()]), "TotalScore"

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
        return empirical_core

    optimized_deck = []
    id_map = {str(c["card_id"]): c for c in pool_cards}
    for cid, var in card_vars.items():
        count = int(var.varValue or 0)
        if count > 0:
            optimized_deck.extend([id_map[cid]] * count)

    return optimized_deck
