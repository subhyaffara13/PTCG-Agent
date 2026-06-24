def get_public_state(game_state: dict, current_turn: int) -> dict:
    """Returns only publicly visible game information."""
    return {
        "my_hand_count": len(game_state.get("my_hand", [])),
        "my_deck_count": game_state.get("my_deck_count", 60),
        "my_prizes": game_state.get("my_prizes", 6),
        "my_active_pokemon": game_state.get("my_active_pokemon"),
        "my_bench": game_state.get("my_bench", []),
        "my_active_damage": game_state.get("my_active_damage", 0),
        "opponent_active": game_state.get("opponent_active"),
        "opponent_bench_count": len(game_state.get("opponent_bench", [])),
        "opponent_prizes": game_state.get("opponent_prizes", 6),
        "opponent_discard": game_state.get("opponent_discard", []),
        "turn_number": current_turn,
        "legal_attacks": game_state.get("legal_attacks", []),
        "legal_attachments": game_state.get("legal_attachments", []),
        "legal_bench": game_state.get("legal_bench", []),
        "legal_evolutions": game_state.get("legal_evolutions", []),
        "legal_trainers": game_state.get("legal_trainers", [])
    }
