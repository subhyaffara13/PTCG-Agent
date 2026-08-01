
def state_to_tensor(game_state: dict) -> np.ndarray:
    """Convert game state dict → 20-element float32 feature vector."""
    my_prizes = float(game_state.get("my_prizes", 6)) / 6.0
    opp_prizes = float(game_state.get("opponent_prizes", 6)) / 6.0
    my_active_hp = game_state.get("my_active_hp", 100) / 100.0
    opp_active_hp = game_state.get("opponent_active_hp", 100) / 100.0

    active = game_state.get("my_active_pokemon", {}) or {}
    attached = float(len(active.get("attached", []) or active.get("energies", []))) / 10.0

    my_bench = game_state.get("my_bench", [])
    opp_bench = game_state.get("opponent_bench", [])
    my_bench_size = float(len(my_bench) if isinstance(my_bench, list) else 0) / 5.0
    opp_bench_size = float(len(opp_bench) if isinstance(opp_bench, list) else 0) / 5.0

    my_hand = game_state.get("my_hand", [])
    my_hand_size = float(len(my_hand) if isinstance(my_hand, list) else 0) / 10.0

    turn = float(game_state.get("turn_number", 0)) / 20.0

    my_discard = game_state.get("my_discard_pile", [])
    opp_discard = game_state.get("opponent_discard_pile", [])
    my_discard_size = float(len(my_discard) if isinstance(my_discard, list) else 0) / 60.0
    opp_discard_size = float(len(opp_discard) if isinstance(opp_discard, list) else 0) / 60.0

    stadium = 1.0 if game_state.get("stadium_card") else 0.0

    weakness_mult = 0.0
    resistance_mult = 0.0
    opp_active = game_state.get("opponent_active_pokemon", {}) or {}
    if isinstance(active, dict) and isinstance(opp_active, dict):
        my_type = active.get("element_type", "")
        opp_weakness = opp_active.get("weakness", "")
        opp_resistance = opp_active.get("resistance", "")
        if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
            weakness_mult = 1.0
        if my_type and opp_resistance and my_type.lower() == opp_resistance.lower():
            resistance_mult = 1.0

    features = [
        my_prizes, opp_prizes, my_active_hp, opp_active_hp, attached,
        my_bench_size, opp_bench_size, my_hand_size, turn,
        my_discard_size, opp_discard_size, stadium,
        weakness_mult, resistance_mult,
    ] + [0.0] * 6

    return np.array(features, dtype=np.float32)

