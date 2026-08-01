
def apply_attacker_bonus(score, counts):
    attackers = counts.get("attackers", [])
    num_attackers = len(attackers) if isinstance(attackers, list) else 0
    if num_attackers >= 4:
        score += 0.10
    elif num_attackers >= 2:
        score += 0.05
    elif num_attackers <= 0:
        score -= 0.30
    fast_attackers = sum(1 for a in (attackers if isinstance(attackers, list) else []) if getattr(a, 'energy_cost', 3) <= 2)
    if fast_attackers >= 3:
        score += 0.10
    elif fast_attackers >= 1:
        score += 0.05
    return score

