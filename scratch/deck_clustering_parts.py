"""Helper functions extracted from deck_clustering.py."""

import re


def normalize(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u00e9", "e").replace("\u00e8", "e")
    text = text.replace("\u00e0", "a").replace("\u00f1", "n")
    text = re.sub(r"[^a-z0-9' ]+", "", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_priority_set(names: list, pool_cards: list) -> set:
    norm_targets = {normalize(n) for n in names}
    matches = set()
    for c in pool_cards:
        if normalize(c.get("card_name", "")) in norm_targets:
            matches.add(str(c["card_id"]))
    return matches
