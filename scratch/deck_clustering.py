import logging
from collections import Counter

from scratch.deck_clustering_parts import normalize, build_priority_set

logger = logging.getLogger(__name__)

ARCHETYPE_TOP_K = {
    "aggro": 200,
    "combo": 200,
    "control": 200,
    "utility": 200,
}

_STAPLE_TRAINERS = [
    "Ultra Ball", "Nest Ball", "Quick Ball", "Level Ball",
    "Switch", "Switch Cart", "Super Rod", "Pal Pad",
    "Boss's Orders", "Professor's Research", "Iono", "Judge",
    "Arven", "Buddy-Buddy Poffin", "Rare Candy", "Hilda",
    "Lillie's Determination", "Pokegear 3.0", "Poke Pad",
]

ARCHETYPE_PRIORITY_CARD_NAMES = {
    "aggro": [
        "Basic {R} Energy", "Basic {W} Energy", "Basic {L} Energy",
        "Basic {F} Energy", "Basic {D} Energy",
        "Double Turbo Energy", "Gift Energy",
    ] + _STAPLE_TRAINERS,
    "combo": [
        "Basic {P} Energy", "Basic {L} Energy", "Basic {G} Energy",
        "Jet Energy", "Double Turbo Energy",
    ] + _STAPLE_TRAINERS,
    "control": [
        "Basic {P} Energy", "Basic {D} Energy",
        "Jet Energy", "Reversal Energy",
    ] + _STAPLE_TRAINERS,
    "utility": [
        "Basic {L} Energy", "Basic {W} Energy",
        "Jet Energy", "Double Turbo Energy",
    ] + _STAPLE_TRAINERS,
}


def filter_pool_by_archetype(pool_cards: list, details: dict,
                              archetype: str = "aggro",
                              top_k: int = None) -> list:
    if top_k is None:
        top_k = ARCHETYPE_TOP_K.get(archetype, 200)

    seen_ids = set()
    candidates = []

    for c in pool_cards:
        cid = str(c["card_id"])
        if c.get("archetype") == archetype and cid not in seen_ids:
            candidates.append(c)
            seen_ids.add(cid)

    candidates.sort(key=lambda c: float(c.get("ev_score", 0.0)), reverse=True)

    selected_raw = candidates[:top_k]
    selected_ids = {str(c["card_id"]) for c in selected_raw}

    for c in list(selected_raw):
        prev = details.get(str(c["card_id"]), {}).get("previous_stage")
        if prev:
            prevo = next(
                (x for x in pool_cards
                 if normalize(x.get("card_name", "")) == normalize(prev)
                 and str(x["card_id"]) not in selected_ids),
                None
            )
            if prevo:
                selected_raw.append(prevo)
                selected_ids.add(str(prevo["card_id"]))

    priority_ids = build_priority_set(
        ARCHETYPE_PRIORITY_CARD_NAMES.get(archetype, []), pool_cards)
    for c in pool_cards:
        cid = str(c["card_id"])
        if cid in selected_ids:
            continue
        is_priority = cid in priority_ids
        is_basic_energy = c.get("card_type") == "Energy" and "basic" in normalize(c.get("card_name", ""))
        if is_priority or is_basic_energy:
            selected_raw.append(c)
            selected_ids.add(cid)

    logger.info(
        f"Clustering: filtered {len(pool_cards)} -> {len(selected_raw)} cards "
        f"for archetype={archetype}"
    )
    return selected_raw
