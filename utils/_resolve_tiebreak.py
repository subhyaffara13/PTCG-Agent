
def _resolve_tiebreak(robots):
    """Cascade: total energy → unit count → 0.5/0.5 draw. Returns (reward_0, reward_1).

    Loser is -1 (not 0) so the Kaggle episode panel's rank logic doesn't
    misclassify the loser's reward as missing and label both players "Tie".
    """
    energy = [0, 0]
    units = [0, 0]
    for r in robots.values():
        energy[r["owner"]] += r["energy"]
        units[r["owner"]] += 1
    if energy[0] != energy[1]:
        return (1, -1) if energy[0] > energy[1] else (-1, 1)
    if units[0] != units[1]:
        return (1, -1) if units[0] > units[1] else (-1, 1)
    return (0.5, 0.5)

