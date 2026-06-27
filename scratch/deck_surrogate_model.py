import logging

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class DeckFitnessMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def _build_card_index(pool_cards):
    seen = {}
    index = []
    for c in pool_cards:
        cid = str(c["card_id"])
        if cid not in seen:
            seen[cid] = len(index)
            index.append(c)
    return index, seen


def _deck_to_tensor(deck, card_index, size):
    vec = torch.zeros(size)
    for c in deck:
        idx = card_index.get(str(c["card_id"]))
        if idx is not None:
            vec[idx] += 1.0
    return vec


def _max_copies_tensor(cards):
    return torch.tensor([
        99.0 if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "") else 4.0
        for c in cards
    ], dtype=torch.float32)
