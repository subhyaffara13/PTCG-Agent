"""
cb_agents/ppo_trainer_network.py

Defines the ActorCritic neural network architecture for PPO.
Uses a Transformer encoder over card token sequences (hand/active/bench/discard)
to learn card synergies, with scalar features appended after CLS aggregation.
Falls back to a flat MLP if PyTorch is unavailable.
"""

import logging
from cb_agents.state_dimensions import (
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
            self.cls_embed = nn.Parameter(torch.zeros(1, 1, CARD_EMBED_DIM))
            nn.init.normal_(self.cls_embed, 0.0, 0.02)

            encoder_layer = nn.TransformerEncoderLayer(
                d_model=CARD_EMBED_DIM,
                nhead=ATTN_HEADS,
                dim_feedforward=TRANSFORMER_FF_DIM,
                batch_first=True
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=TRANSFORMER_LAYERS)
            self.project = nn.Linear(CARD_EMBED_DIM + SCALAR_FEATURES, hidden_dim)
            self.norm = nn.LayerNorm(hidden_dim)

        def forward(self, token_ids: torch.Tensor, zone_ids: torch.Tensor, scalars: torch.Tensor, padding_mask: torch.Tensor | None = None) -> torch.Tensor:
            """
            token_ids: (B, T) card token IDs
            zone_ids:  (B, T) zone IDs
            scalars:   (B, SCALAR_FEATURES) float scalar features
            padding_mask: (B, T+1) bool mask where True indicates PADDING to ignore
            """
            B = token_ids.size(0)
            x = self.card_embed(token_ids) + self.zone_embed(zone_ids)  # (B, T, D)
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
        def __init__(self, input_dim: int = STATE_DIM, hidden_dim: int = 128, action_dim: int = 3000, state_dim: int | None = None):
            super().__init__()
            if state_dim is not None:
                input_dim = state_dim
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

        def forward(self, x=None, token_ids=None, zone_ids=None, scalars=None, padding_mask=None):
            """
            If token_ids is provided, uses the Transformer encoder.
            Otherwise falls back to the flat MLP base.
            Returns: (logits, value)
            """
            if token_ids is not None:
                features = self.encoder(token_ids, zone_ids, scalars, padding_mask)
                logits = self.actor(features)
                value = self.critic(features)
            else:
                if x is None:
                    B = 1
                    x = torch.zeros(B, STATE_DIM)
                features = self.flat_base(x)
                logits = self.flat_actor(features)
                value = self.flat_critic(features)
            return logits, value

        def get_action_and_value(self, state: torch.Tensor, action: torch.Tensor | None = None):
            B = state.size(0)
            logits, value = self.forward(x=state)
            dist = torch.distributions.Categorical(logits=logits)
            if action is None:
                action = dist.sample()
            log_prob = dist.log_prob(action)
            entropy = dist.entropy()
            return action, log_prob, entropy, value.squeeze(-1)

        def get_value(self, state: torch.Tensor) -> torch.Tensor:
            _, value = self.forward(x=state)
            return value.squeeze(-1)

        def load_state_dict(self, state_dict, strict=False, assign=False):
            mapped_dict = {}
            for k, v in state_dict.items():
                if k.startswith("transformer_encoder."):
                    mapped_dict[k.replace("transformer_encoder.", "encoder.", 1)] = v
                elif k.startswith("base."):
                    mapped_dict[k.replace("base.", "flat_base.", 1)] = v
                elif k.startswith("actor.0."):
                    mapped_dict[k.replace("actor.0.", "flat_actor.", 1)] = v
                elif k.startswith("critic.0."):
                    mapped_dict[k.replace("critic.0.", "flat_critic.", 1)] = v
                else:
                    mapped_dict[k] = v
            return super().load_state_dict(mapped_dict, strict=False)

else:
    class ActorCritic:
        def __init__(self, *args, **kwargs):
            pass
        def to(self, *args, **kwargs):
            return self
        def load_state_dict(self, *args, **kwargs):
            pass
        def eval(self, *args, **kwargs):
            return self
        def parameters(self, *args, **kwargs):
            return []
        def __call__(self, *args, **kwargs):
            return None, None
