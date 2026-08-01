
def perform_weight_upgrade(weights: dict, direction: int, lr: float = 0.1) -> dict:
    new_weights = dict(weights)
    for w, scale in [("prize_weight", 0.5), ("hand_weight", 0.2), ("board_weight", 0.3),
                     ("energy_weight", 0.4), ("evolution_combo_weight", 0.2), ("trainer_utility_weight", 0.1)]:
        new_weights[w] = max(0.1, new_weights[w] + lr * direction * scale)
    return new_weights

