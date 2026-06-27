import logging

import numpy as np

from scratch.deck_embedding_utils import (
    _ELEMENT_TYPES,
    _STAGES,
    _ARCHETYPES,
    _COMBO_TAGS,
    _build_card_embedding,
    _feature_dim,
    build_embedding_index,
    _archetype_centroids,
    decode_embedding,
)

logger = logging.getLogger(__name__)


def search_novel_archetype(pool_cards, details, scores, evaluate_fn, iters=200):
    cards, embeddings = build_embedding_index(pool_cards, details)
    centroids = _archetype_centroids(cards, embeddings)
    rng = np.random.default_rng(42)
    best_deck, best_fit = None, -float("inf")
    for t in range(iters):
        src_arch = rng.choice(_ARCHETYPES)
        base = centroids.get(src_arch, np.zeros(_feature_dim()))
        noise_scale = 2.0 * (1.0 - t / iters) + 0.5
        offset = rng.uniform(-noise_scale, noise_scale, size=_feature_dim())
        away = np.zeros(_feature_dim())
        for arch in _ARCHETYPES:
            c = centroids.get(arch)
            if c is not None:
                diff = base - c
                away += diff / (np.linalg.norm(diff) + 1e-8)
        target = base + offset + 0.3 * away
        deck = decode_embedding(target, cards, embeddings, rng)
        if len(deck) != 60:
            continue
        try:
            fit = evaluate_fn((deck, scores, details))
            if fit > best_fit:
                best_fit = fit
                best_deck = list(deck)
        except Exception as e:
            logger.warning("Evaluation failed at iteration %d: %s", t, e)
    return best_deck, best_fit


__all__ = [
    "_ELEMENT_TYPES", "_STAGES", "_ARCHETYPES", "_COMBO_TAGS",
    "_build_card_embedding", "_feature_dim", "build_embedding_index",
    "_archetype_centroids", "decode_embedding", "search_novel_archetype",
]
