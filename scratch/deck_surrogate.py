import logging

import torch

from scratch.deck_surrogate_model import DeckFitnessMLP, _build_card_index, _deck_to_tensor, _max_copies_tensor
from scratch.deck_surrogate_train import build_training_data, train_surrogate_model, _decode_continuous, optimize_via_surrogate

logger = logging.getLogger(__name__)


class SurrogateDeckOptimizer:
    def __init__(self, pool_cards, details, scores):
        self.pool_cards = pool_cards
        self.details = details
        self.scores = scores
        self.model = None
        self.cards = None
        self.card_index = None
        self.max_cp = None
        logger.info("SurrogateDeckOptimizer initialized with %d pool cards", len(pool_cards))

    def score_deck(self, deck):
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
        try:
            vec = _deck_to_tensor(deck, self.card_index, len(self.cards)) / self.max_cp
            with torch.no_grad():
                return self.model(vec.unsqueeze(0)).item()
        except Exception as e:
            logger.error("Failed to score deck: %s", e)
            raise

    def train(self, pool_cards=None, details=None, scores=None, **kwargs):
        p = pool_cards or self.pool_cards
        d = details or self.details
        s = scores or self.scores
        self.model, self.cards, self.card_index, self.max_cp = train_surrogate_model(p, d, s, **kwargs)
        return self

    def optimize(self, pool_cards=None, details=None, scores=None, **kwargs):
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
        p = pool_cards or self.pool_cards
        d = details or self.details
        s = scores or self.scores
        return optimize_via_surrogate(self.model, self.cards, self.card_index, self.max_cp, p, d, s, **kwargs)


__all__ = [
    "DeckFitnessMLP", "_build_card_index", "_deck_to_tensor", "_max_copies_tensor",
    "build_training_data", "train_surrogate_model", "_decode_continuous", "optimize_via_surrogate",
    "SurrogateDeckOptimizer",
]
