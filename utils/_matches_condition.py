
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

