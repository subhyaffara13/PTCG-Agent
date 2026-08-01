
def apply_learned_rules(score: float, deck: list, counts: dict,
                        learned_dos: dict, learned_donts: dict) -> float:
    """Adjust *score* based on learned pattern rules."""
    # Reward: boost score for cards matching learned 'do' patterns
    for do in learned_dos.get("deck_dos", []):
        if any(str(c.get("card_id")) == str(do.get("card_id")) for c in deck):
            score += min(0.05, 0.01 * do.get("avg_count", 1.0))

    # Penalize: subtract penalty for matching 'don't' conditions
    e_c = counts["eng"]
    t_c = counts["item"] + counts["sup"]
    p_c = counts["pkmn"]

    for rule in learned_donts.get("deck_donts", []):
        cond = rule.get("condition", "")
        penalty = rule.get("penalty", 5.0)
        if _matches_condition(cond, e_c, t_c, p_c):
            score -= penalty

    # Deck-out risk penalty: too many draw supporters burn through the deck
    score -= _deck_out_risk(deck, counts)

    # Attacker bonus: ensure deck can win by prizes, not just deck-out
    attackers = counts.get("attackers", [])
    num_attackers = len(attackers) if isinstance(attackers, list) else 0
    if num_attackers >= 4:
        score += 0.10  # Enough attackers to consistently take prizes
    elif num_attackers >= 2:
        score += 0.05  # Bare minimum attackers
    elif num_attackers <= 0:
        score -= 0.30  # No attackers! Can only win by deck-out — fragile strategy
    # Reward attacker energy efficiency: attackers with cost <= 2 are faster
    fast_attackers = sum(1 for a in (attackers if isinstance(attackers, list) else []) if getattr(a, 'energy_cost', 3) <= 2)
    if fast_attackers >= 3:
        score += 0.10
    elif fast_attackers >= 1:
        score += 0.05

    return score

