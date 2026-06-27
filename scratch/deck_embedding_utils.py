import logging
from collections import Counter

import numpy as np

logger = logging.getLogger(__name__)

_ELEMENT_TYPES = ["{R}", "{W}", "{G}", "{L}", "{F}", "{P}", "{D}", "{M}"]
_STAGES = ["Basic", "Stage 1", "Stage 2"]
_ARCHETYPES = ["aggro", "control", "combo", "utility"]
_COMBO_TAGS = ["search", "discard", "attach", "energy", "draw", "shuffle",
               "bench", "switch", "heal", "damage", "evolve"]


def _build_card_embedding(c, details):
    det = details.get(c["card_id"], {})
    stage = det.get("stage", "Basic")
    etype = det.get("element_type", "")
    feat = []
    ct = c.get("card_type", "")
    feat.append(1.0 if ct == "Pokemon" else 0.0)
    feat.append(1.0 if ct == "Trainer" else 0.0)
    feat.append(1.0 if ct == "Energy" else 0.0)
    feat.extend([1.0 if et == etype else 0.0 for et in _ELEMENT_TYPES])
    feat.extend([1.0 if s == stage else 0.0 for s in _STAGES])
    a = c.get("archetype", "utility")
    feat.extend([1.0 if a == arch else 0.0 for arch in _ARCHETYPES])
    feat.append(float(c.get("ev_score", 0.0)))
    feat.append(float(c.get("utility_score", 0.0)))
    feat.append(float(c.get("deck_frequency", 0.0)))
    feat.append(min(1.0, float(c.get("energy_cost", 0)) / 5.0))
    feat.append(min(1.0, float(c.get("damage_output", 0)) / 300.0))
    tags = {str(t).lower() for t in c.get("combo_tags", [])}
    feat.extend([1.0 if tag in tags else 0.0 for tag in _COMBO_TAGS])
    return np.array(feat, dtype=np.float64)


def _feature_dim():
    return (3 + len(_ELEMENT_TYPES) + len(_STAGES) + len(_ARCHETYPES) + 5 + len(_COMBO_TAGS))


def build_embedding_index(pool_cards, details):
    unique = {}
    for c in pool_cards:
        cid = c["card_id"]
        if cid not in unique:
            unique[cid] = c
    cards = list(unique.values())
    dim = _feature_dim()
    embeddings = np.zeros((len(cards), dim), dtype=np.float64)
    for i, c in enumerate(cards):
        embeddings[i] = _build_card_embedding(c, details)
    return cards, embeddings


def _archetype_centroids(cards, embeddings):
    centroids = {}
    for arch in _ARCHETYPES:
        mask = [i for i, c in enumerate(cards) if c.get("archetype") == arch]
        if mask:
            centroids[arch] = embeddings[mask].mean(axis=0)
    return centroids


def decode_embedding(target, cards, embeddings, rng):
    deck = []
    copies = Counter()
    n = len(cards)
    target = target.copy()
    num_pokemon = rng.integers(10, 17)
    num_energy = rng.integers(8, 15)
    num_trainer = 60 - num_pokemon - num_energy
    order = ["pokemon"] * num_pokemon + ["energy"] * num_energy + ["trainer"] * num_trainer
    rng.shuffle(order)
    for needed_type in order:
        best = None
        best_dist = float("inf")
        for i in range(n):
            c = cards[i]
            ct = c.get("card_type")
            if (ct == "Pokemon") != (needed_type == "pokemon"):
                continue
            if (ct == "Trainer") != (needed_type == "trainer"):
                continue
            if (ct == "Energy") != (needed_type == "energy"):
                continue
            cid = c["card_id"]
            limit = 99 if (ct == "Energy" and "Basic" in c.get("card_name", "")) else 4
            if copies[cid] >= limit:
                continue
            dist = np.linalg.norm(embeddings[i] - target)
            if dist < best_dist:
                best_dist = dist
                best = i
        if best is not None:
            deck.append(cards[best])
            copies[cards[best]["card_id"]] += 1
    return deck[:60]
