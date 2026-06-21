"""
factory/deck_scorer.py

Scores candidate decks on consistency, prize efficiency, recovery, and matchup spread.
Applies archetype-specific weights and learned do/don't rules.
"""

import math
from typing import List, Dict, Any
from factory.deck_scorer_rules import apply_learned_rules


class DeckScorer:
    def __init__(self, card_details: dict, learned_dos: dict, learned_donts: dict):
        self.card_details = card_details
        self.learned_dos = learned_dos
        self.learned_donts = learned_donts

    def score_candidate(self, deck: List[dict], archetype: str = "aggro") -> dict:
        counts = self._count_categories(deck)
        consistency = self._consistency_score(deck, counts)
        prize_eff = self._prize_efficiency(deck, counts)
        recovery = self._recovery_score(counts)
        match_spread = self._matchup_spread(deck, counts)

        weights = {"aggro": (0.40, 0.40, 0.10, 0.10), "control": (0.25, 0.15, 0.30, 0.30),
                   "combo": (0.50, 0.20, 0.15, 0.15)}.get(archetype, (0.30, 0.20, 0.25, 0.25))
        score = consistency * weights[0] + prize_eff * weights[1] + recovery * weights[2] + match_spread * weights[3]
        score = apply_learned_rules(score, deck, counts, self.learned_dos, self.learned_donts)

        return {"deck_score": round(max(0.0, score), 4), "metrics": {
            "consistency_score": round(consistency, 4), "prize_efficiency_score": round(prize_eff, 4),
            "recovery_score": round(recovery, 4), "matchup_spread_score": round(match_spread, 4)}}

    def _count_categories(self, deck):
        basic = s1 = s2 = sup = item = eng = rec = 0
        attackers = []
        for c in deck:
            ct = c.get("card_type")
            det = self.card_details.get(str(c.get("card_id")), {})
            stage = det.get("stage")
            if ct == "Pokemon":
                if stage == "Basic": basic += 1
                elif stage == "Stage 1": s1 += 1
                elif stage == "Stage 2": s2 += 1
                if c.get("energy_cost", 0) > 0: attackers.append(c)
            elif ct == "Energy": eng += 1
            elif ct == "Trainer":
                if "Supporter" in c.get("combo_tags", ["Supporter"]): sup += 1
                else: item += 1
            if "discard" in c.get("combo_tags", []): rec += 1
        return {"basic": basic, "s1": s1, "s2": s2, "sup": sup, "item": item,
                "eng": eng, "rec": rec, "attackers": attackers, "pkmn": basic + s1 + s2}

    def _consistency_score(self, deck, ct):
        prob_brick = math.comb(60 - ct["basic"], 7) / math.comb(60, 7) if ct["basic"] <= 53 else 0.0
        prob_open = 1.0 - prob_brick
        cs = min(1.0, max(0.0, (ct["basic"] / 60) * (ct["sup"] / 60) * 2.0))
        if prob_open < 0.85: cs = max(0.0, cs - 0.3)
        names = {c.get("card_name", "").lower() for c in deck}
        evo_pen = sum(0.05 for c in deck if c.get("card_type") == "Pokemon" and
                      self.card_details.get(str(c["card_id"]), {}).get("previous_stage") and
                      self.card_details.get(str(c["card_id"]), {}).get("previous_stage").lower() not in names)
        pyr = (0.15 if ct["s1"] > 0 and ct["basic"] <= ct["s1"] else 0) + \
              (0.15 if ct["s2"] > 0 and ct["s1"] <= ct["s2"] else 0)
        cs = max(0.0, cs - evo_pen - pyr)
        if ct["item"] < ct["sup"] and ct["sup"] > 0: cs = max(0.0, cs - 0.1)
        atk3 = sum(1 for a in ct["attackers"] if a.get("energy_cost", 0) >= 3)
        accel = sum(1 for c in deck if "attach" in str(c.get("combo_tags", "")).lower())
        if atk3 > 0 and accel < 2: cs = max(0.0, cs - 0.25)
        return cs

    def _prize_efficiency(self, deck, ct):
        atk = ct["attackers"]
        pe = min(1.0, sum(a.get("damage_output", 0) / max(1, a.get("energy_cost", 1)) for a in atk) / len(atk) / 100) if atk else 0.0
        req = {self.card_details.get(str(c["card_id"]), {}).get("element_type", "") for c in deck if c.get("card_type") == "Pokemon"}
        req.discard("")
        mm = sum(0.02 for e in deck if e.get("card_type") == "Energy" and "Basic" in e.get("card_name", "")
                 and not any(r in e.get("card_name", "") for r in req) and req)
        return max(0.0, pe - mm)

    def _recovery_score(self, ct):
        rs = min(1.0, ct["sup"] / 15.0)
        return min(1.0, rs + 0.1) if ct["rec"] >= 2 else (max(0.0, rs - 0.1) if ct["rec"] == 0 else rs)

    def _matchup_spread(self, deck, ct):
        ms = 0.8
        gust = sum(1 for c in deck if "gust" in str(c.get("combo_tags", "")).lower() or "switch" in str(c.get("combo_tags", "")).lower())
        if gust == 0: ms = max(0.0, ms - 0.2)
        return ms
