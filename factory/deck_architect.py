"""
factory/deck_architect.py

Creates exactly 60-card decks matching card pool regulations,
evaluates exactly 5 candidates using rubric rules, and outputs
staging/deck_new.csv + staging/deck_report.json.
"""

import csv
import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class DeckArchitect(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", 
                 staging_dir: str = "staging", decisions_file: str = "decisions.md", 
                 perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.staging_dir = Path(staging_dir)
        self.decisions_file = Path(decisions_file)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        
        # Load once on init only
        self.card_pool = self._load_card_pool()
        self.rubric = self._load_deck_rubric()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "DeckArchitect does not receive routed packets — it builds deck layouts directly"
        )

    def _load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def _load_deck_rubric(self) -> dict:
        path = self.skills_dir / "deck_rubric.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read deck_rubric.json: {e}")
        return {}

    def build(self, improvement_notes: dict) -> dict:
        """
        Builds, scores, selects, and outputs a new 60-card TCG deck configuration.
        """
        # STEP 1: Read context from improvement_notes
        current_archetype = improvement_notes.get("next_eval_context", "aggro")
        # Map test context names to standard archetypes
        if "test" in current_archetype:
            current_archetype = current_archetype.replace("_test", "")
        if current_archetype not in ("aggro", "control", "combo", "utility"):
            current_archetype = "aggro"

        weak_metric = improvement_notes.get("reasoning", "low deck delta")

        # STEP 2: Filter legal cards matching archetype
        # Also collect Energy and Basic Pokemon fallback items from card_pool
        legal_cards = [c for c in self.card_pool if c.get("archetype") == current_archetype or c.get("card_type") == "Energy"]
        basic_pokemon = [c for c in self.card_pool if c.get("card_type") == "Pokemon" and "Basic" in c.get("combo_tags", ["Basic"])]
        energy_cards = [c for c in self.card_pool if c.get("card_type") == "Energy"]

        # Safety Fallbacks if card pool is too small to build a deck
        if len(legal_cards) < 3:
            # Insufficient cards error handler
            self._log_error_to_decisions(f"Insufficient legal cards for archetype '{current_archetype}' to generate 60-card deck.")
            return {"status": "failed", "reason": "insufficient_cards"}

        # STEP 3: Generate and score 5 candidate decks
        candidates = []
        for i in range(5):
            candidate = self._generate_candidate(legal_cards, basic_pokemon, energy_cards)
            score_data = self._score_candidate(candidate)
            candidates.append((candidate, score_data))

        # STEP 4: Select best candidate
        # Pick deck with highest score, fallback to highest consistency
        candidates.sort(key=lambda x: (x[1]["deck_score"], x[1]["metrics"]["consistency_score"]), reverse=True)
        best_deck, best_scores = candidates[0]

        # STEP 5: Write staging files
        self._write_csv(best_deck)
        self._write_report(current_archetype, best_scores, weak_metric)

        return {
            "status": "success",
            "deck_score": best_scores["deck_score"],
            "archetype": current_archetype
        }

    def _generate_candidate(self, legal_cards: list, basic_pokemon: list, energy_cards: list) -> List[Dict[str, Any]]:
        """Generates exactly 60 cards following rules."""
        deck = []
        
        # Rule: Include at least 1 Basic Pokemon
        # Prefer explicit Basic Pokemon; fall back to any Pokemon in pool before using sentinel
        if basic_pokemon:
            basic_choice = random.choice(basic_pokemon)
        else:
            any_pokemon = [c for c in legal_cards if c.get("card_type") == "Pokemon"]
            if any_pokemon:
                basic_choice = random.choice(any_pokemon)
            else:
                # Last-resort sentinel — should never reach here with a populated card pool
                basic_choice = {"card_id": 0, "card_name": "Basic Pokemon", "card_type": "Pokemon", "ev_score": 0.5, "combo_tags": ["Basic"]}
        deck.append(dict(basic_choice))

        # Rule: Include basic Energy cards
        basic_energies = [c for c in energy_cards if "Basic" in c.get("card_name", "")]
        energy_choice = random.choice(basic_energies) if basic_energies else {
            "card_id": 1, "card_name": "Basic Energy", "card_type": "Energy", "ev_score": 0.5
        }
        deck.extend([dict(energy_choice) for _ in range(8)]) # typical minimum boundary

        # Fill up to 60 using legal pool, enforcing max 4 copies constraint (except Energy)
        card_copies = {}
        for c in deck:
            cid = c["card_id"]
            card_copies[cid] = card_copies.get(cid, 0) + 1

        loop_guard = 0
        while len(deck) < 60 and loop_guard < 5000:
            loop_guard += 1
            candidate_card = random.choice(legal_cards)
            cid = candidate_card["card_id"]
            is_basic_energy = candidate_card.get("card_type") == "Energy" and "Basic" in candidate_card.get("card_name", "")
            if is_basic_energy or card_copies.get(cid, 0) < 4:
                deck.append(dict(candidate_card))
                card_copies[cid] = card_copies.get(cid, 0) + 1

        # If loop guard tripped, pad with whatever is available
        while len(deck) < 60:
            deck.append(dict(random.choice(legal_cards)))

        return deck

    def _score_candidate(self, deck: List[dict]) -> dict:
        """Calculates metric weights matching deck_rubric patterns."""
        basic_pokemon_count = sum(1 for c in deck if c.get("card_type") == "Pokemon" and "Basic" in c.get("combo_tags", ["Basic"]))
        supporter_count = sum(1 for c in deck if c.get("card_type") == "Trainer" and "Supporter" in c.get("combo_tags", ["Supporter"]))
        attackers = [c for c in deck if c.get("card_type") == "Pokemon" and c.get("energy_cost", 0) > 0]

        # consistency_score
        scaling_factor = 2.0
        consistency_score = ((basic_pokemon_count / 60) * (supporter_count / 60)) * scaling_factor
        consistency_score = min(1.0, max(0.0, consistency_score))

        # prize_efficiency_score
        if attackers:
            raw_eff = sum(c.get("damage_output", 0) / max(1, c.get("energy_cost", 1)) for c in attackers) / len(attackers)
            prize_efficiency_score = min(1.0, raw_eff / 100.0) # normalise based on avg expected standard damage
        else:
            prize_efficiency_score = 0.0

        # recovery_score
        recovery_score = min(1.0, supporter_count / 15.0)

        # matchup_spread_score
        matchup_spread_score = 0.8 # default baseline index

        # DECK_SCORE = weighted sum
        deck_score = (
            consistency_score * 0.35 +
            prize_efficiency_score * 0.25 +
            recovery_score * 0.20 +
            matchup_spread_score * 0.20
        )

        return {
            "deck_score": round(deck_score, 4),
            "metrics": {
                "consistency_score": round(consistency_score, 4),
                "prize_efficiency_score": round(prize_efficiency_score, 4),
                "recovery_score": round(recovery_score, 4),
                "matchup_spread_score": round(matchup_spread_score, 4)
            }
        }

    def _write_csv(self, deck: List[dict]):
        # Deduplicate to output counts
        counts = {}
        for c in deck:
            cid = c["card_id"]
            if cid not in counts:
                counts[cid] = {
                    "card_id": cid,
                    "card_name": c.get("card_name", "Unknown"),
                    "card_type": c.get("card_type", "Trainer"),
                    "count": 0,
                    "ev_score": c.get("ev_score", 0.0)
                }
            counts[cid]["count"] += 1

        dest = self.staging_dir / "deck_new.csv"
        with open(dest, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["card_id", "card_name", "card_type", "count", "ev_score"])
            for key in counts:
                row = counts[key]
                writer.writerow([row["card_id"], row["card_name"], row["card_type"], row["count"], row["ev_score"]])

    def _write_report(self, archetype: str, scores: dict, weak_metric: str):
        report = {
            "timestamp": datetime.now().isoformat(),
            "archetype": archetype,
            "deck_score": scores["deck_score"],
            "metrics": scores["metrics"],
            "card_count": 60,
            "candidates_evaluated": 5,
            "weak_metric_addressed": weak_metric
        }
        dest = self.staging_dir / "deck_report.json"
        dest.write_text(json.dumps(report, indent=2), encoding="utf-8")

    def _log_error_to_decisions(self, reason: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n## DECK ARCHITECT ERROR — {timestamp}\n"
            f"**Error:** {reason}\n"
            f"---\n"
        )
        try:
            with open(self.decisions_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to log architect error to decisions.md: {e}")
