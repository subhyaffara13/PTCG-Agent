"""
factory/deck_generator.py

Generates 60-card decks using archetype-aware construction with evolution pyramids,
consistency trainers, and hypergeometric setup validation.
"""

import random
from typing import List, Dict, Any
from factory.deck_generator_helpers import (
    hypergeometric_setup_prob, add_card,
    inject_signature_cards, inject_evolution_pyramids,
    inject_consistency_trainers, enforce_bounds, fill_to_60,
)


class DeckGenerator:
    def __init__(self, card_pool: list, card_details: dict, archetypes_data: dict):
        self.card_pool = card_pool
        self.card_details = card_details
        self.archetypes_data = archetypes_data

    def generate_candidate(self, legal_cards: list, basic_pokemon: list,
                           energy_cards: list, archetype: str) -> List[Dict[str, Any]]:
        """Build a 60-card deck for *archetype* from *legal_cards*."""
        deck, copies = [], {}
        ctr = {"pkmn": 0, "supporter": 0, "energy": 0, "discard": 0}

        id_map = {str(c["card_id"]): c for c in self.card_pool}
        name_map = {c["card_name"].lower(): c for c in self.card_pool}
        arch = self.archetypes_data.get("archetypes", {}).get(archetype, {})

        # Core skeleton: signature + evolution + consistency
        inject_signature_cards(arch, id_map, name_map, deck, copies, ctr)
        inject_evolution_pyramids(deck, self.card_details, name_map, copies, ctr)
        inject_consistency_trainers(deck, self.card_details, id_map, name_map, copies, ctr)
        enforce_bounds(legal_cards, basic_pokemon, name_map, deck, copies, ctr,
                       self.card_pool, self.card_details)

        # Energies
        matching = self._matching_energies(deck, energy_cards)
        lim = 0
        while ctr["energy"] < 12 and len(deck) < 60 and lim < 100:
            if add_card(random.choice(matching), 1, deck, copies, ctr) == 0:
                lim += 1

        # Fill to 60 + pad
        fill_to_60(legal_cards, matching, deck, copies, ctr, self.card_details)
        while len(deck) < 60:
            deck.append(dict(random.choice(matching or legal_cards)))

        # Hypergeometric validation: >= 95% chance of Basic in opening hand
        basics = sum(1 for c in deck if c.get("card_type") == "Pokemon"
                     and self.card_details.get(str(c["card_id"]), {}).get("stage") == "Basic")
        if hypergeometric_setup_prob(60, basics) < 0.95 and basic_pokemon:
            for _ in range(5):
                if hypergeometric_setup_prob(60, basics) >= 0.95:
                    break
                add_card(random.choice(basic_pokemon), 1, deck, copies, ctr)
                basics += 1
        return deck[:60]

    def _matching_energies(self, deck, energy_cards):
        """Find basic energies matching the element types in the deck."""
        req = {self.card_details.get(str(c["card_id"]), {}).get("element_type", "")
               for c in deck if c.get("card_type") == "Pokemon"}
        req.discard("")
        if not req:
            req.add("{W}")
        basic_e = [c for c in energy_cards if "Basic" in c.get("card_name", "")]
        return ([e for e in basic_e if any(r in e.get("card_name", "") for r in req)]
                or basic_e
                or [{"card_id": "1", "card_name": "Basic Energy", "card_type": "Energy", "ev_score": 0.5}])
