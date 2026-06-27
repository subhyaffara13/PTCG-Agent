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
class DeckScorer:
    def __init__(self, card_details: dict, learned_dos: dict, learned_donts: dict, weights_config: dict = None):
        self.card_details = card_details
        self.learned_dos = learned_dos
        self.learned_donts = learned_donts
        self.weights_config = weights_config if weights_config is not None else dict(DEFAULT_ARCHETYPE_WEIGHTS)

    def score_candidate(self, deck: List[dict], archetype: str = "aggro") -> dict:
        cards = [CardState.from_dict(c, self.card_details) for c in deck]
        counts = self._count_categories(cards)
        consistency = self._consistency_score(cards, counts)
        prize_eff = self._prize_efficiency(cards, counts)
        recovery = self._recovery_score(counts)
        match_spread = self._matchup_spread(cards, counts)

        graph = get_global_synergy_graph()
        synergy_raw = score_deck_synergy(deck, graph)
        synergy_norm = min(1.0, max(0.0, synergy_raw / 100.0))

        weights = self.weights_config.get(archetype, (0.25, 0.20, 0.20, 0.20, 0.15))
        score = consistency * weights[0] + prize_eff * weights[1] + recovery * weights[2] + match_spread * weights[3]
        if len(weights) > 4:
            score += synergy_norm * weights[4]
            
        score = apply_learned_rules(score, deck, counts, self.learned_dos, self.learned_donts)

        return {"deck_score": round(max(0.0, score), 4), "metrics": {
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
                if "supporter" in c.combo_tags: sup += 1
                else: item += 1
            if "discard" in c.combo_tags: rec += 1
        return {"basic": basic, "s1": s1, "s2": s2, "sup": sup, "item": item,
                "eng": eng, "rec": rec, "attackers": attackers, "pkmn": basic + s1 + s2}

    def _consistency_score(self, deck: List[CardState], ct: dict):
        prob_brick = math.comb(60 - ct["basic"], 7) / math.comb(60, 7) if ct["basic"] <= 53 else 0.0
        prob_open = 1.0 - prob_brick
        cs = min(1.0, max(0.0, (ct["basic"] / 60) * (ct["sup"] / 60) * 2.0))
        if prob_open < 0.85: cs = max(0.0, cs - 0.3)
        names = {c.card_name for c in deck}
        evo_pen = sum(0.05 for c in deck if c.card_type == "Pokemon" and
                      c.previous_stage and
                      c.previous_stage not in names)
        pyr = (0.15 if ct["s1"] > 0 and ct["basic"] <= ct["s1"] else 0) + \
              (0.15 if ct["s2"] > 0 and ct["s1"] <= ct["s2"] else 0)
        cs = max(0.0, cs - evo_pen - pyr)
        if ct["item"] < ct["sup"] and ct["sup"] > 0: cs = max(0.0, cs - 0.1)
        atk3 = sum(1 for a in ct["attackers"] if a.energy_cost >= 3)
        accel = sum(1 for c in deck if "attach" in c.combo_tags)
        if atk3 > 0 and accel < 2: cs = max(0.0, cs - 0.25)
        return cs

    def _prize_efficiency(self, deck: List[CardState], ct: dict):
        atk = ct["attackers"]
        pe = min(1.0, sum(a.damage_output / max(1, a.energy_cost) for a in atk) / len(atk) / 100) if atk else 0.0
        req = {c.element_type for c in deck if c.card_type == "Pokemon"}
        req.discard("")
        mm = sum(0.02 for e in deck if e.card_type == "Energy" and "basic" in e.card_name
                 and not any(r in e.card_name for r in req) and req)
        return max(0.0, pe - mm)

    def _recovery_score(self, ct: dict):
        rs = min(1.0, ct["sup"] / 15.0)
        return min(1.0, rs + 0.1) if ct["rec"] >= 2 else (max(0.0, rs - 0.1) if ct["rec"] == 0 else rs)

    def _matchup_spread(self, deck: List[CardState], ct: dict):
        ms = 0.8
        gust = sum(1 for c in deck if "gust" in c.combo_tags or "switch" in c.combo_tags)
        if gust == 0: ms = max(0.0, ms - 0.2)
        return ms
