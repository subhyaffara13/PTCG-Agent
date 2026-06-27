from dataclasses import dataclass
from typing import List, Dict
from collections import Counter
from scratch.deck_synergy_graph import get_global_synergy_graph, score_deck_synergy

@dataclass
class CardPackage:
    name: str                    # e.g. "Charizard Engine"
    cards: Dict[int, int]        # card_id → count
    total_cards: int
    package_type: str            # "engine", "attacker", "trainer_core", "energy", "tech"
    synergy_score: float         # internal package synergy

class BeamDeckBuilder:
    def __init__(self, packages: List[CardPackage], beam_width: int = 10):
        self.packages = packages
        self.beam_width = beam_width
        self.graph = get_global_synergy_graph()
        
    def build(self, id_map: dict) -> List[dict]:
        beam = [{
            "deck": [],
            "cards": Counter(),
            "score": 0.0,
            "size": 0
        }]
        
        for step in range(6):
            new_beam = []
            for state in beam:
                # Always allow not adding a package to keep existing good partial decks
                new_beam.append(state)
                
                for pkg in self.packages:
                    if state["size"] + pkg.total_cards > 55:  # Leave room for MILP to finish it
                        continue
                        
                    new_cards = state["cards"].copy()
                    valid = True
                    for cid, count in pkg.cards.items():
                        new_cards[cid] += count
                        card = id_map.get(cid, {})
                        limit = 60 if card.get("card_type") == "Energy" and "Basic" in card.get("card_name", "") else 4
                        if new_cards[cid] > limit:
                            valid = False
                            break
                    
                    if not valid:
                        continue
                        
                    new_deck = list(state["deck"])
                    for cid, count in pkg.cards.items():
                        if cid in id_map:
                            new_deck.extend([id_map[cid]] * count)
                            
                    score = score_deck_synergy(new_deck, self.graph)
                    new_beam.append({
                        "deck": new_deck,
                        "cards": new_cards,
                        "score": score,
                        "size": state["size"] + pkg.total_cards
                    })
                    
            if not new_beam:
                break
                
            new_beam.sort(key=lambda x: x["score"], reverse=True)
            # Remove duplicates based on cards
            unique_beam = []
            seen = set()
            for b in new_beam:
                k = frozenset(b["cards"].items())
                if k not in seen:
                    seen.add(k)
                    unique_beam.append(b)
            beam = unique_beam[:self.beam_width]
            
        if not beam:
            return []
            
        # Return best partial deck (we can pad it or let MILP pad it later)
        return beam[0]["deck"]


def extract_packages(id_map: dict) -> List[CardPackage]:
    graph = get_global_synergy_graph()
    engines = graph.extract_core_engines(threshold=1.5)
    packages = []
    
    for i, eng in enumerate(engines):
        cards = {cid: 2 for cid in eng} # Assign 2 copies heuristically
        total_cards = sum(cards.values())
        if total_cards > 15:
            continue
            
        dummy_deck = []
        for cid, count in cards.items():
            if cid in id_map:
                dummy_deck.extend([id_map[cid]] * count)
                
        syn_score = score_deck_synergy(dummy_deck, graph)
        packages.append(CardPackage(
            name=f"AutoEngine_{i}",
            cards=cards,
            total_cards=total_cards,
            package_type="engine",
            synergy_score=syn_score
        ))
        
    return packages
