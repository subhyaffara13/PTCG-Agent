"""Shared dimensions for aligned state tensors."""

MAX_HAND = 20
MAX_BOARD = 20
MAX_PRIZES = 6
MAX_OPP_VISIBLE = 20
META_FEATURES = 5

SINGLE_STATE_DIM = MAX_HAND + MAX_BOARD + MAX_PRIZES + MAX_OPP_VISIBLE + META_FEATURES
STACK_SIZE = 3
STATE_DIM = SINGLE_STATE_DIM * STACK_SIZE

# Transformer value network constants
CARD_VOCAB_SIZE = 4096     # max card IDs (padded for safety)
CARD_EMBED_DIM = 32        # embedding dimension per card token
MAX_TOKENS = 32            # max card tokens fed to Transformer (hand + bench + discard sample + active)
SCALAR_FEATURES = 6        # prize counts (×2), HP (×2), turn, weakness flag
TRANSFORMER_LAYERS = 2     # number of TransformerEncoder layers
ATTN_HEADS = 4             # number of self-attention heads
TRANSFORMER_FF_DIM = 64    # feedforward hidden size inside each Transformer layer

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

