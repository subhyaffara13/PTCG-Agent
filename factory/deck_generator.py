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
        """Mutate a seed deck by randomly swapping out cards while maintaining 60 cards, evolution dependencies, basic counts, and 4-copy rule."""
        if not legal_cards or len(seed_deck) != 60:
            return seed_deck
        new_deck = [dict(c) for c in seed_deck]
        
        for _ in range(num_swaps):
            # 1. Identify valid cards to remove without leaving orphaned evolutions
            valid_remove_indices = [
                idx for idx in range(len(new_deck))
                if self._can_remove_card(new_deck, idx)
            ]
            
            if not valid_remove_indices:
                break
                
            remove_idx = random.choice(valid_remove_indices)
            removed_card = new_deck.pop(remove_idx)
            
            # 2. Find valid replacement cards that fit energy types, 4-copy rule, and evolution pyramid
            valid_replacements = [
                c for c in legal_cards 
                if self._is_valid_replacement(c, new_deck, legal_cards)
            ]
            
            if valid_replacements:
                # If basic pokemon count is below 12, prioritize basic pokemon replacements
                basics_count = sum(
                    1 for c in new_deck 
                    if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"
                )
                if basics_count < 12:
                    basic_replacements = [
                        c for c in valid_replacements 
                        if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"
                    ]
                    if basic_replacements:
                        valid_replacements = basic_replacements

                new_card = random.choice(valid_replacements)
                new_deck.append(dict(new_card))
            else:
                # Revert removal if no valid replacement exists
                new_deck.insert(remove_idx, removed_card)
            
        # Ensure at least 12 basic pokemon in mutated deck to guarantee >= 90% setup probability
        basics_count = sum(
            1 for c in new_deck 
            if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"
        )
        if basics_count < 12 and basic_pokemon:
            needed = 12 - basics_count
            for _ in range(needed):
                removable_indices = [
                    idx for idx in range(len(new_deck))
                    if self._can_remove_card(new_deck, idx) and not (
                        new_deck[idx].get("card_type") == "Pokemon" and 
                        self.card_details.get(str(new_deck[idx].get("card_id")), {}).get("stage") == "Basic"
                    )
                ]
                if not removable_indices:
                    break
                rem_idx = random.choice(removable_indices)
                new_deck.pop(rem_idx)
                
                valid_b = [
                    b for b in basic_pokemon 
                    if self._is_valid_replacement(b, new_deck, legal_cards)
                ]
                if valid_b:
                    new_deck.append(dict(random.choice(valid_b)))
                elif basic_pokemon:
                    new_deck.append(dict(random.choice(basic_pokemon)))
            
        return new_deck[:60]

    def _can_remove_card(self, deck: list, remove_idx: int) -> bool:
        """Check if removing card at remove_idx leaves any orphaned evolution card."""
        card = deck[remove_idx]
        if card.get("card_type") != "Pokemon":
            return True
            
        deck_after = deck[:remove_idx] + deck[remove_idx+1:]
        remaining_pokemon_names = {
            c.get("card_name", "").lower() 
            for c in deck_after if c.get("card_type") == "Pokemon"
        }
        
        for c in deck_after:
            if c.get("card_type") == "Pokemon":
                det = self.card_details.get(str(c.get("card_id")), {})
                stage = det.get("stage") or c.get("stage")
                if stage in ("Stage 1", "Stage 2"):
                    prev = det.get("previous_stage") or c.get("previous_stage")
                    if prev and prev.lower() not in remaining_pokemon_names:
                        return False
        return True

    def _is_valid_replacement(self, candidate: dict, deck: list, legal_cards: list) -> bool:
        """Verify replacement card fits 4-copy rule, deck's energy types, and evolution pyramid."""
        cid = str(candidate.get("card_id"))
        cname = str(candidate.get("card_name", ""))
        ctype = candidate.get("card_type")
        det = self.card_details.get(cid, {})

        # 1. 4-copy rule check (except basic energy)
        is_basic_energy = (ctype == "Energy" and "Basic" in cname)
        current_copies = sum(1 for d in deck if str(d.get("card_name", "")) == cname)
        if not is_basic_energy and current_copies >= 4:
            return False

        # 2. Energy type check: if energy card, must match deck's attacking pokemon types
        if ctype == "Energy":
            matching = self._matching_energies(deck, legal_cards)
            matching_ids = {str(m.get("card_id")) for m in matching}
            matching_names = {m.get("card_name") for m in matching}
            if cid not in matching_ids and cname not in matching_names:
                return False

        # 3. Evolution pyramid check if candidate is a Pokemon
        if ctype == "Pokemon":
            stage = det.get("stage") or candidate.get("stage", "Basic")
            deck_pokemon_names = {
                d.get("card_name", "").lower() 
                for d in deck if d.get("card_type") == "Pokemon"
            }

            if stage in ("Stage 1", "Stage 2"):
                prev = det.get("previous_stage") or candidate.get("previous_stage")
                if not prev or prev.lower() not in deck_pokemon_names:
                    return False

            # Check pyramid ratio bounds
            bc = sum(
                1 for d in deck 
                if d.get("card_type") == "Pokemon" and self.card_details.get(str(d.get("card_id")), {}).get("stage") == "Basic"
            )
            s1 = sum(
                1 for d in deck 
                if d.get("card_type") == "Pokemon" and self.card_details.get(str(d.get("card_id")), {}).get("stage") == "Stage 1"
            )
            s2 = sum(
                1 for d in deck 
                if d.get("card_type") == "Pokemon" and self.card_details.get(str(d.get("card_id")), {}).get("stage") == "Stage 2"
            )

            if stage == "Stage 1" and (s1 + 1 > bc):
                return False
            if stage == "Stage 2" and (s2 + 1 > s1):
                return False

        return True

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
        legal_basics = [b for b in basic_pokemon if b in legal_cards or
                        self.card_details.get(str(b.get("card_id")), {}).get("element_type") in core_elements]
        basic_candidates = legal_basics or basic_pokemon
        if basic_candidates:
            target_basics = basics
            while target_basics < 20 and self.hypergeometric_setup_prob(60, target_basics) < 0.95:
                target_basics += 1
            for _ in range(target_basics - basics):
                self.add_card(random.choice(basic_candidates), 1, deck, copies, ctr)
                
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
        """Find basic energies matching the element types of attacking Pokémon in the deck."""
        element_to_keywords = {
            "{G}": {"grass", "{g}"},
            "{R}": {"fire", "{r}"},
            "{W}": {"water", "{w}"},
            "{L}": {"lightning", "{l}"},
            "{P}": {"psychic", "{p}"},
            "{F}": {"fighting", "{f}"},
            "{D}": {"darkness", "dark", "{d}"},
            "{M}": {"metal", "{m}"},
            "Grass": {"grass", "{g}"},
            "Fire": {"fire", "{r}"},
            "Water": {"water", "{w}"},
            "Lightning": {"lightning", "{l}"},
            "Psychic": {"psychic", "{p}"},
            "Fighting": {"fighting", "{f}"},
            "Darkness": {"darkness", "dark", "{d}"},
            "Metal": {"metal", "{m}"},
        }

        req_keywords = set()
        for c in deck:
            if c.get("card_type") == "Pokemon":
                det = self.card_details.get(str(c.get("card_id")), {})
                elem = det.get("element_type", "") or c.get("element_type", "")
                elem_str = str(elem).strip()
                if not elem_str or elem_str in ("{C}", "Colorless"):
                    continue
                has_dmg = c.get("damage_output") if c.get("damage_output") is not None else det.get("damage_output")
                has_cost = c.get("energy_cost") if c.get("energy_cost") is not None else det.get("energy_cost")
                if has_dmg == 0 and has_cost == 0:
                    continue
                kw_set = element_to_keywords.get(elem_str)
                if kw_set:
                    req_keywords.update(kw_set)

        basic_e = [c for c in energy_cards if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "")]
        if not basic_e:
            basic_e = [c for c in energy_cards if c.get("card_type") == "Energy"]

        matched = []
        if req_keywords:
            for e in basic_e:
                ename = e.get("card_name", "").lower()
                edet = self.card_details.get(str(e.get("card_id")), {})
                eelem = str(edet.get("element_type", "") or e.get("element_type", "")).lower()
                if any(kw in ename or kw == eelem for kw in req_keywords):
                    matched.append(e)

        if matched:
            return matched
        return basic_e or [{"card_id": 6, "card_name": "Basic Lightning Energy", "card_type": "Energy", "ev_score": 0.5}]
