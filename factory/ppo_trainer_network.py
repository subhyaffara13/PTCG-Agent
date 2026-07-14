"""
factory/ppo_trainer_network.py

Defines the ActorCritic neural network architecture for PPO.
Uses a Transformer encoder over card token sequences (hand/active/bench/discard)
to learn card synergies, with scalar features appended after CLS aggregation.
Falls back to a flat MLP if PyTorch is unavailable.
"""

import logging
from factory.state_dimensions import (
    STATE_DIM, CARD_VOCAB_SIZE, CARD_EMBED_DIM, MAX_TOKENS,
    SCALAR_FEATURES, TRANSFORMER_LAYERS, ATTN_HEADS, TRANSFORMER_FF_DIM,
)

logger = logging.getLogger(__name__)

# Special token IDs (above card vocab range)
PAD_TOKEN = 0
CLS_TOKEN = CARD_VOCAB_SIZE - 1  # 4095
SEP_TOKEN = CARD_VOCAB_SIZE - 2  # 4094

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available. ActorCritic model cannot be defined.")

if TORCH_AVAILABLE:
    class CardTransformerEncoder(nn.Module):
        """
        Encodes a variable-length sequence of card tokens via self-attention.
        Prepends a learnable [CLS] token; its final representation is used
        as the board state embedding.

        Architecture:
          Embedding(CARD_VOCAB_SIZE, CARD_EMBED_DIM)
          + Learned type-zone positional encoding (hand/active/bench/discard)
          -> TransformerEncoder(TRANSFORMER_LAYERS layers, ATTN_HEADS heads)
          -> CLS output (CARD_EMBED_DIM) concatenated with SCALAR_FEATURES
          -> Linear(CARD_EMBED_DIM + SCALAR_FEATURES -> hidden_dim)
        """
        ZONE_COUNT = 4  # hand, active, bench, discard
        ZONE_HAND = 0
        ZONE_ACTIVE = 1
        ZONE_BENCH = 2
        ZONE_DISCARD = 3

        def __init__(self, hidden_dim: int = 128):
            super().__init__()
            self.card_embed = nn.Embedding(CARD_VOCAB_SIZE, CARD_EMBED_DIM, padding_idx=PAD_TOKEN)
            self.zone_embed = nn.Embedding(self.ZONE_COUNT, CARD_EMBED_DIM)
            # CLS token embedding (learnable)
            self.cls_embed = nn.Parameter(torch.zeros(1, 1, CARD_EMBED_DIM))
            nn.init.normal_(self.cls_embed, std=0.02)

            encoder_layer = nn.TransformerEncoderLayer(
                d_model=CARD_EMBED_DIM,
                nhead=ATTN_HEADS,
                dim_feedforward=TRANSFORMER_FF_DIM,
                dropout=0.1,
                batch_first=True,
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=TRANSFORMER_LAYERS)
            self.project = nn.Linear(CARD_EMBED_DIM + SCALAR_FEATURES, hidden_dim)
            self.norm = nn.LayerNorm(hidden_dim)

        def forward(self, token_ids: torch.Tensor, zone_ids: torch.Tensor,
                    scalars: torch.Tensor, padding_mask: torch.Tensor) -> torch.Tensor:
            """
            Args:
                token_ids: (B, MAX_TOKENS) int64 card IDs (0 = PAD)
                zone_ids:  (B, MAX_TOKENS) int64 zone tags (0=hand,1=active,2=bench,3=discard)
                scalars:   (B, SCALAR_FEATURES) float32 prize/HP/turn features
                padding_mask: (B, MAX_TOKENS+1) bool True=ignore (includes CLS slot)
            Returns:
                (B, hidden_dim) state embedding
            """
            B = token_ids.size(0)
            x = self.card_embed(token_ids) + self.zone_embed(zone_ids)  # (B, T, D)
            # Prepend CLS token
            cls = self.cls_embed.expand(B, -1, -1)                      # (B, 1, D)
            x = torch.cat([cls, x], dim=1)                              # (B, T+1, D)

            x = self.transformer(x, src_key_padding_mask=padding_mask)  # (B, T+1, D)
            cls_out = x[:, 0, :]                                         # (B, D)

            combined = torch.cat([cls_out, scalars], dim=-1)             # (B, D+SCALAR)
            return self.norm(self.project(combined))                     # (B, hidden_dim)

    class ActorCritic(nn.Module):
        """
        Transformer-based Actor-Critic.
        Shared Transformer backbone encodes the board as card tokens.
        Actor head outputs logits over action vocabulary.
        Critic head outputs a scalar state value.
        """
        def __init__(self, input_dim: int = STATE_DIM, hidden_dim: int = 128, action_dim: int = 3000):
            super().__init__()
            # Transformer backbone
            self.encoder = CardTransformerEncoder(hidden_dim=hidden_dim)
            # MLP fallback base (used when token tensors are not available)
            self.flat_base = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim // 2),
            )
            # Actor and Critic heads
            self.actor = nn.Linear(hidden_dim, action_dim)
            self.critic = nn.Linear(hidden_dim, 1)
            # Flat critic path (when using flat_base)
            self.flat_critic = nn.Linear(hidden_dim // 2, 1)
            self.flat_actor = nn.Linear(hidden_dim // 2, action_dim)

        def forward(self, x, token_ids=None, zone_ids=None, scalars=None, padding_mask=None):
            """
            If token_ids is provided, uses the Transformer encoder.
            Otherwise falls back to the flat MLP base (for compatibility with old PPO data).
            Returns: (logits, value)
            """
            if token_ids is not None:
                features = self.encoder(token_ids, zone_ids, scalars, padding_mask)
                logits = self.actor(features)
                value = self.critic(features)
            else:
                features = self.flat_base(x)
                logits = self.flat_actor(features)
                value = self.flat_critic(features)
            return logits, value

        def load_state_dict(self, state_dict, strict=True, assign=False):
            # Map legacy MLP keys to the new 'flat_' keys for backward compatibility
            mapped_dict = {}
            for k, v in state_dict.items():
                if k.startswith("base."):
                    mapped_dict[k.replace("base.", "flat_base.", 1)] = v
                elif k.startswith("actor.0."):
                    mapped_dict[k.replace("actor.0.", "flat_actor.", 1)] = v
                elif k.startswith("critic.0."):
                    mapped_dict[k.replace("critic.0.", "flat_critic.", 1)] = v
                else:
                    mapped_dict[k] = v
            # Use strict=False so the new Transformer (encoder) can start from scratch
            return super().load_state_dict(mapped_dict, strict=False)


else:
    class ActorCritic:
        def __init__(self, *args, **kwargs):
            pass
