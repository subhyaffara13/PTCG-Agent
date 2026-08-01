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

from utils.encode_state_vector import encode_state_vector

