"""
factory/deck_scorer.py

Scores candidate decks on consistency, prize efficiency, recovery, and matchup spread.
Applies archetype-specific weights and learned do/don't rules.
"""

import math
from typing import List, Dict
from factory.deck_scorer_rules import apply_learned_rules
from factory.configs import DEFAULT_ARCHETYPE_WEIGHTS
from factory.deck_scorer_state import CardState
from scratch.deck_synergy_graph import get_global_synergy_graph, score_deck_synergy

from factory.deck_scorer_consistency import consistency_score, recovery_score
from factory.deck_scorer_efficiency import prize_efficiency
from factory.deck_scorer_matchup import matchup_spread
class DeckScorer:
    def __init__(self, card_details: dict, learned_dos: dict, learned_donts: dict, weights_config: dict | None = None):
        self.card_details = card_details
        self.learned_dos = learned_dos
        self.learned_donts = learned_donts
        self.weights_config = weights_config if weights_config is not None else dict(DEFAULT_ARCHETYPE_WEIGHTS)

    def score_candidate(self, deck: List[dict], archetype: str = "aggro") -> dict:
        cards = [CardState.from_dict(c, self.card_details) for c in deck]
        counts = self._count_categories(cards)
        consistency = consistency_score(deck=cards, ct=counts)
        prize_eff = prize_efficiency(deck=cards, ct=counts)
        recovery = recovery_score(ct=counts)
        match_spread = matchup_spread(deck=cards, ct=counts)

        graph = get_global_synergy_graph()
        synergy_raw = score_deck_synergy(deck, graph)
        synergy_norm = min(1.0, max(0.0, synergy_raw / 100.0))

        weights = self.weights_config.get(archetype, (0.25, 0.20, 0.20, 0.20, 0.15))
        score = consistency * weights[0] + prize_eff * weights[1] + recovery * weights[2] + match_spread * weights[3]
        if len(weights) > 4:
            score += synergy_norm * weights[4]
            
        score = apply_learned_rules(score, deck, counts, self.learned_dos, self.learned_donts)

        return {"deck_score": round(min(1.0, max(0.0, score)), 4), "metrics": {
            "consistency_score": round(consistency, 4), "prize_efficiency_score": round(prize_eff, 4),
            "recovery_score": round(recovery, 4), "matchup_spread_score": round(match_spread, 4),
            "synergy_score": round(synergy_norm, 4)}}
    def _count_categories(self, deck: List[CardState]):
        basic = s1 = s2 = sup = item = eng = rec = 0
        attackers = []
        for c in deck:
            if c.card_type == "Pokemon":
                if c.stage == "Basic": basic += 1
                elif c.stage == "Stage 1": s1 += 1
                elif c.stage == "Stage 2": s2 += 1
                if c.energy_cost > 0: attackers.append(c)
            elif c.card_type == "Energy": eng += 1
            elif c.card_type == "Trainer":
                name = c.card_name.lower()
                supporters = {"judge", "professor's research", "iono", "boss's orders", "arven", "serena", 
                              "colress's tenacity", "erika's invitation", "jacq", "nemona", "cynthia", 
                              "marnie", "volkner", "skyla", "n", "juniper", "sycamore", "kiara"}
                if "supporter" in c.combo_tags or any(s in name for s in supporters): sup += 1
                else: item += 1
            if "discard" in c.combo_tags: rec += 1
        return {"basic": basic, "s1": s1, "s2": s2, "sup": sup, "item": item,
                "eng": eng, "rec": rec, "attackers": attackers, "pkmn": basic + s1 + s2}

