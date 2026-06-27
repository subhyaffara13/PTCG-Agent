def calculate_player_score(p_data: dict, weights: dict, card_names: dict, card_types: dict, evolution_predecessors: dict) -> float:
    if not p_data or not isinstance(p_data, dict):
        return 0.0
    prizes_taken = 6 - len(p_data.get("prize", []) or [])
    hand_list = p_data.get("hand", []) or []
    active = p_data.get("active", []) or []
    bench = p_data.get("bench", []) or []
    
    energy_attached = sum(len(b.get("attached", []) or []) for b in bench if isinstance(b, dict))
    active_hp = 0
    if active and isinstance(active[0], dict):
        energy_attached += len(active[0].get("attached", []) or [])
        active_hp += active[0].get("hp", 0) or 0

    evolve_combos = trainer_utility = 0
    board_names = {card_names.get(str(x["id"])) for x in (active + bench) if isinstance(x, dict) and "id" in x}
    board_names.discard(None)

    for h in hand_list:
        if isinstance(h, dict) and "id" in h:
            hid = str(h["id"])
            if card_names.get(hid) in evolution_predecessors:
                if evolution_predecessors[card_names[hid]] in board_names:
                    evolve_combos += 1
            if card_types.get(hid) == "Trainer":
                trainer_utility += 1

    return (
        weights.get("prize_weight", 2.0) * prizes_taken +
        weights.get("hand_weight", 0.5) * len(hand_list) +
        weights.get("board_weight", 1.0) * (len(active) + len(bench)) +
        weights.get("energy_weight", 1.5) * energy_attached +
        weights.get("active_hp_weight", 0.01) * active_hp +
        weights.get("evolution_combo_weight", 0.8) * evolve_combos +
        weights.get("trainer_utility_weight", 0.4) * trainer_utility
    )

def perform_weight_upgrade(weights: dict, direction: int, lr: float = 0.1) -> dict:
    new_weights = dict(weights)
    for w, scale in [("prize_weight", 0.5), ("hand_weight", 0.2), ("board_weight", 0.3),
                     ("energy_weight", 0.4), ("evolution_combo_weight", 0.2), ("trainer_utility_weight", 0.1)]:
        new_weights[w] = max(0.1, new_weights[w] + lr * direction * scale)
    return new_weights
