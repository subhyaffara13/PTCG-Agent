"""
factory/deck_scorer_rules.py

Applies learned do/don't rules to adjust deck scores.
"""

_DRAW_SUPPORTER_NAMES = {"professor's research", "carmine", "lillie",
                         "iono", "judge", "n", "juniper", "sycamore",
                         "colress", "colress's tenacity", "nemona"}


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


def _deck_out_risk(deck: list, counts: dict) -> float:
    draw_count = 0
    for c in deck:
        name = str(c.get("card_name", "")).lower()
        if any(ds in name for ds in _DRAW_SUPPORTER_NAMES):
            draw_count += 1

    est_draw_total = draw_count * 6.5
    est_natural = 12.0
    est_cards_drawn = est_draw_total + est_natural
    penalty = 0.0
    if est_cards_drawn > 50:
        penalty += 0.10
    if est_cards_drawn > 55:
        penalty += 0.15
    if est_cards_drawn > 60:
        penalty += 0.25
    if draw_count >= 8:
        penalty += 0.10
    if draw_count >= 12:
        penalty += 0.25
    return min(penalty, 0.6)


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
    if cond == "energy_lt_10" and e_c < 10:
        return True
    if cond == "energy_lt_12" and e_c < 12:
        return True
    return False
