"""
factory/deck_architect.py
Evaluates exactly 5 candidates using rubric rules, and outputs staging/deck_new.csv + staging/deck_report.json.
"""
import json
import logging
from pathlib import Path
from typing import Any, List, Dict
from cb_agents.base_agent import BaseAgent
from factory.deck_loader import DeckLoader
from factory.deck_generator import DeckGenerator
from factory.deck_scorer import DeckScorer
from factory.deck_architect_helpers import write_deck_csv, write_deck_report, log_error_to_decisions

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
        
        self.learned_donts = self._load_json(self.skills_dir / "learned_donts.json", "deck_donts")
        self.learned_dos = self._load_json(self.skills_dir / "learned_dos.json", "deck_dos")
        
        loader = DeckLoader(self.skills_dir)
        self.card_pool = loader.load_card_pool()
        self.rubric = loader.load_deck_rubric()
        self.archetypes_data = loader.load_archetypes_data()
        self.card_details = loader.parse_card_details(self.card_pool)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("DeckArchitect does not receive routed packets")

    def _load_json(self, path: Path, key: str) -> dict:
        if path.exists():
            try: return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e: logger.error(f"Failed to load {path.name}: {e}")
        return {key: []}

    def build(self, improvement_notes: dict) -> dict:
        current_archetype = improvement_notes.get("next_eval_context", "aggro")
        # Read metagame distribution report if available to auto-select counter archetype
        meta_dist_path = self.log_dir / "metagame_distribution.json"
        if meta_dist_path.exists():
            try:
                meta_info = json.loads(meta_dist_path.read_text(encoding="utf-8"))
                dominant_meta = meta_info.get("dominant_meta", "")
                if dominant_meta == "Fire":
                    current_archetype = "combo"  # Water beats Fire 2x
                elif dominant_meta == "Lightning":
                    current_archetype = "aggro"  # Fighting/Aggro counter
                elif dominant_meta == "Control":
                    current_archetype = "aggro"  # Fast Aggro counters Control
            except Exception:
                pass
        if "test" in current_archetype:
            current_archetype = current_archetype.replace("_test", "")
        if current_archetype not in ("aggro", "control", "combo", "utility"):
            current_archetype = "aggro"

        weak_metric = improvement_notes.get("reasoning", "low deck delta")
        legal_cards = [c for c in self.card_pool if not c.get("archetype") or c.get("archetype") in (current_archetype, "all", "utility", "") or str(c.get("card_type", "")).upper() in ("ENERGY", "TRAINER")]
        basic_pokemon = [c for c in self.card_pool if str(c.get("card_type", "")).upper() == "POKEMON" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"]
        energy_cards = [c for c in self.card_pool if str(c.get("card_type", "")).upper() == "ENERGY"]

        if len(legal_cards) < 3:
            log_error_to_decisions(f"Insufficient legal cards for archetype '{current_archetype}'", self.decisions_file)
            return {"status": "failed", "reason": "insufficient_cards"}

        from factory.deck_architect_helpers import read_deck_csv
        import math
        import random

        generator = DeckGenerator(self.card_pool, self.card_details, self.archetypes_data)
        scorer = DeckScorer(self.card_details, self.learned_dos, self.learned_donts)

        # 1. Load seed decks (only if all cards are present in current card pool)
        card_pool_ids = {str(c.get("card_id")) for c in self.card_pool}
        seed_paths = [self.skills_dir / f"league/{current_archetype}_exploiter.csv", Path("cb_agents/deck_new.csv")]
        seed_decks = []
        for p in seed_paths:
            if p.exists():
                d = read_deck_csv(p)
                if len(d) == 60 and all(str(c.get("card_id")) in card_pool_ids for c in d):
                    seed_decks.append(d)

        if seed_decks:
            # Score seeds to find the best starting point
            scored_seeds = [(d, scorer.score_candidate(d, current_archetype)) for d in seed_decks]
            scored_seeds.sort(key=lambda x: x[1]["deck_score"], reverse=True)
            current_deck, current_scores = scored_seeds[0]
        else:
            # Fallback
            current_deck = generator.generate_candidate(legal_cards, basic_pokemon, energy_cards, current_archetype)
            current_scores = scorer.score_candidate(current_deck, current_archetype)

        best_deck = [dict(c) for c in current_deck]
        best_scores = dict(current_scores)
        current_score = current_scores["deck_score"]

        # 2. Simulated Annealing
        temp = 1.0
        cooling_rate = 0.90
        iterations = 100

        for _ in range(iterations):
            num_swaps = random.randint(1, 3)
            candidate = generator.mutate_deck(current_deck, num_swaps, legal_cards, basic_pokemon)
            cand_scores = scorer.score_candidate(candidate, current_archetype)
            cand_score = cand_scores["deck_score"]

            # Accept if better
            if cand_score > current_score:
                current_deck = candidate
                current_score = cand_score
                if cand_score > best_scores["deck_score"]:
                    best_deck = [dict(c) for c in candidate]
                    best_scores = cand_scores
            else:
                # Accept slightly worse occasionally to escape local maxima
                acceptance_prob = math.exp((cand_score - current_score) / max(temp, 0.01))
                if random.random() < acceptance_prob:
                    current_deck = candidate
                    current_score = cand_score

            temp *= cooling_rate

        write_deck_csv(best_deck, self.staging_dir / "deck_new.csv")
        write_deck_report(current_archetype, best_scores, weak_metric, self.staging_dir / "deck_report.json")

        return {"status": "success", "deck_score": best_scores["deck_score"], "archetype": current_archetype}
