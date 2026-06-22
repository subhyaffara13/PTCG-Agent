"""
factory/deck_scorer_rules.py

Applies learned do/don't rules to adjust deck scores.
"""


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

    return score


def _matches_condition(cond: str, e_c: int, t_c: int, p_c: int) -> bool:
    """Check if a deck composition matches a don't-rule condition."""
    if cond == "energy_gt_25_trainer_lt_10" and e_c > 25 and t_c < 10:
        return True
    if cond == "pokemon_gt_30" and p_c > 30:
        return True
    if cond == "pokemon_lt_12" and p_c < 12:
        return True
    if cond == "energy_lt_12_trainer_lt_10" and e_c < 12 and t_c < 10:
        return True
    return False
