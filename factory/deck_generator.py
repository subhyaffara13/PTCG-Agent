import random
from typing import List, Dict, Any

from factory.deck_generator_helpers import DeckMathMixin
from factory.deck_generator_injection import DeckInjectionMixin
from factory.deck_generator_bounds import DeckBoundsMixin

class DeckGenerator(DeckMathMixin, DeckInjectionMixin, DeckBoundsMixin):
    def __init__(self, card_pool: list, card_details: dict, archetypes_data: dict):
        self.card_pool = card_pool
        self.card_details = card_details
        self.archetypes_data = archetypes_data

    def mutate_deck(self, seed_deck: List[Dict[str, Any]], num_swaps: int, legal_cards: list, basic_pokemon: list) -> List[Dict[str, Any]]:
        """Mutate a seed deck by randomly swapping out cards while maintaining 60 cards and 4-copy rule."""
        if not legal_cards or len(seed_deck) != 60:
            return seed_deck
        new_deck = [dict(c) for c in seed_deck]
        
        for _ in range(num_swaps):
            # 1. Pick a card to remove
            remove_idx = random.randint(0, len(new_deck) - 1)
            new_deck.pop(remove_idx)
            
            # 2. Re-calculate counts
            counts = {}
            for c in new_deck:
                cname = str(c.get("card_name", ""))
                counts[cname] = counts.get(cname, 0) + 1
            
            # 3. Find valid replacements (must not violate 4-copy rule, unless basic energy)
            valid_replacements = [c for c in legal_cards if (c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "")) or counts.get(str(c.get("card_name", "")), 0) < 4]
            if not valid_replacements:
                valid_replacements = legal_cards
            
            new_card = random.choice(valid_replacements)
            new_deck.append(dict(new_card))
            
        # Ensure at least one basic pokemon
        has_basic = any(c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic" for c in new_deck)
        if not has_basic and basic_pokemon:
            new_deck.pop(random.randint(0, 59))
            new_deck.append(dict(random.choice(basic_pokemon)))
            
        return new_deck

    def generate_candidate(self, legal_cards: list, basic_pokemon: list,
                           energy_cards: list, archetype: str) -> List[Dict[str, Any]]:
        """Build a 60-card deck for *archetype* from *legal_cards*."""
        deck, copies = [], {}
        ctr = {"pkmn": 0, "supporter": 0, "energy": 0, "discard": 0}

        id_map = {str(c["card_id"]): c for c in self.card_pool}
        name_map = {c["card_name"].lower(): c for c in self.card_pool}
        arch = self.archetypes_data.get("archetypes", {}).get(archetype, {})

        # Core skeleton: signature + evolution + consistency
        self.inject_signature_cards(arch, id_map, name_map, deck, copies, ctr)
        self.inject_evolution_pyramids(deck, self.card_details, name_map, copies, ctr)
        self.inject_consistency_trainers(deck, self.card_details, id_map, name_map, copies, ctr)
        self.enforce_bounds(legal_cards, basic_pokemon, name_map, deck, copies, ctr,
                            self.card_pool, self.card_details)

        # Energies
        matching = self._matching_energies(deck, energy_cards)
        if matching:
            needed = min(12 - ctr["energy"], 60 - len(deck))
            for _ in range(max(0, needed)):
                self.add_card(random.choice(matching), 1, deck, copies, ctr)

        # Calculate Core Elements & Tags for Synergy
        core_elements = {self.card_details.get(str(c["card_id"]), {}).get("element_type", "")
                         for c in deck if c.get("card_type") == "Pokemon"}
        core_elements.discard("")
        
        core_tags = set()
        for c in deck:
            core_tags.update(c.get("combo_tags", []))

        # Fill to 60 + pad
        self.fill_to_60(legal_cards, matching, deck, copies, ctr, self.card_details, core_elements, core_tags)
        while len(deck) < 60:
            deck.append(dict(random.choice(matching or legal_cards)))

        # Hypergeometric validation: >= 95% chance of Basic in opening hand
        basics = sum(1 for c in deck if c.get("card_type") == "Pokemon"
                     and self.card_details.get(str(c["card_id"]), {}).get("stage") == "Basic")
        if basic_pokemon:
            target_basics = basics
            while target_basics < 20 and self.hypergeometric_setup_prob(60, target_basics) < 0.95:
                target_basics += 1
            for _ in range(target_basics - basics):
                self.add_card(random.choice(basic_pokemon), 1, deck, copies, ctr)
                
        self.optimize_supporter_count(deck, copies, ctr, legal_cards)
        
        # Hard enforce exactly 60 cards
        if len(deck) > 60:
            deck = deck[:60]
        while len(deck) < 60:
            if matching:
                deck.append(dict(random.choice(matching)))
            elif legal_cards:
                deck.append(dict(random.choice(legal_cards)))
            else:
                break
        
        return deck[:60]

    def optimize_supporter_count(self, deck: list, copies: dict, ctr: dict, legal_cards: list):
        basics = sum(1 for c in deck if c.get("card_type") == "Pokemon"
                     and self.card_details.get(str(c["card_id"]), {}).get("stage") == "Basic")
        supporters = sum(1 for c in deck if self.is_supporter(c))
        
        target_supp = supporters
        while target_supp < 20 and self.turn1_setup_prob(60, basics, target_supp) < 0.85:
            target_supp += 1
            
        supp_pool = [c for c in legal_cards if self.is_supporter(c)]
        if not supp_pool:
            return
            
        for _ in range(target_supp - supporters):
            self.add_card(random.choice(supp_pool), 1, deck, copies, ctr)

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
