
def encode_state_vector(game_state: dict) -> list[float]:
    """Encodes a game state dictionary into a flat float vector of size STATE_DIM (210)."""
    vec = [0.0] * STATE_DIM
    if not isinstance(game_state, dict):
        return vec
    try:
        hand = game_state.get("my_hand", [])
        if isinstance(hand, list):
            for i, cid in enumerate(hand[:MAX_HAND]):
                try:
                    vec[i] = float(cid) if str(cid).isdigit() else 1.0
                except Exception:
                    pass
        vec[MAX_HAND] = float(game_state.get("my_prizes", 6))
        vec[MAX_HAND + 1] = float(game_state.get("opponent_prizes", 6))
        vec[MAX_HAND + 2] = float(game_state.get("my_active_hp", 100)) / 100.0
        vec[MAX_HAND + 3] = float(game_state.get("opponent_active_hp", 100)) / 100.0
        vec[MAX_HAND + 4] = float(game_state.get("turn_number", 1)) / 10.0
    except Exception:
        pass
    return vec


def encode_state_vector(game_state: dict) -> list[float]:
    """Encodes a game state dictionary into a flat float vector of size STATE_DIM (210)."""
    vec = [0.0] * STATE_DIM
    if not isinstance(game_state, dict):
        return vec
    try:
        hand = game_state.get("my_hand", [])
        if isinstance(hand, list):
            for i, cid in enumerate(hand[:MAX_HAND]):
                try:
                    vec[i] = float(cid) if str(cid).isdigit() else 1.0
                except Exception:
                    pass
        vec[MAX_HAND] = float(game_state.get("my_prizes", 6))
        vec[MAX_HAND + 1] = float(game_state.get("opponent_prizes", 6))
        vec[MAX_HAND + 2] = float(game_state.get("my_active_hp", 100)) / 100.0
        vec[MAX_HAND + 3] = float(game_state.get("opponent_active_hp", 100)) / 100.0
        vec[MAX_HAND + 4] = float(game_state.get("turn_number", 1)) / 10.0
    except Exception:
        pass
    return vec


def encode_state_vector(game_state: dict) -> list[float]:
    """Encodes a game state dictionary into a flat float vector of size STATE_DIM (210)."""
    vec = [0.0] * STATE_DIM
    if not isinstance(game_state, dict):
        return vec
    try:
        hand = game_state.get("my_hand", [])
        if isinstance(hand, list):
            for i, cid in enumerate(hand[:MAX_HAND]):
                try:
                    vec[i] = float(cid) if str(cid).isdigit() else 1.0
                except Exception:
                    pass
        vec[MAX_HAND] = float(game_state.get("my_prizes", 6))
        vec[MAX_HAND + 1] = float(game_state.get("opponent_prizes", 6))
        vec[MAX_HAND + 2] = float(game_state.get("my_active_hp", 100)) / 100.0
        vec[MAX_HAND + 3] = float(game_state.get("opponent_active_hp", 100)) / 100.0
        vec[MAX_HAND + 4] = float(game_state.get("turn_number", 1)) / 10.0
    except Exception:
        pass
    return vec

