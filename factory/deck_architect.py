"""
factory/deck_architect.py
Evaluates exactly 5 candidates using rubric rules, and outputs staging/deck_new.csv + staging/deck_report.json.
"""
import json
import logging
from pathlib import Path
from typing import Any, List, Dict
from agents.base_agent import BaseAgent
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
        if "test" in current_archetype:
            current_archetype = current_archetype.replace("_test", "")
        if current_archetype not in ("aggro", "control", "combo", "utility"):
            current_archetype = "aggro"

        weak_metric = improvement_notes.get("reasoning", "low deck delta")
        legal_cards = [c for c in self.card_pool if c.get("archetype") == current_archetype or c.get("card_type") == "Energy" or c.get("card_type") == "Trainer"]
        basic_pokemon = [c for c in self.card_pool if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"]
        energy_cards = [c for c in self.card_pool if c.get("card_type") == "Energy"]

        if len(legal_cards) < 3:
            log_error_to_decisions(f"Insufficient legal cards for archetype '{current_archetype}'", self.decisions_file)
            return {"status": "failed", "reason": "insufficient_cards"}

        generator = DeckGenerator(self.card_pool, self.card_details, self.archetypes_data)
        scorer = DeckScorer(self.card_details, self.learned_dos, self.learned_donts)

        candidates = []
        for _ in range(50):
            cand = generator.generate_candidate(legal_cards, basic_pokemon, energy_cards, current_archetype)
            score_data = scorer.score_candidate(cand, current_archetype)
            candidates.append((cand, score_data))

        candidates.sort(key=lambda x: (x[1]["deck_score"], x[1]["metrics"]["consistency_score"]), reverse=True)
        best_deck, best_scores = candidates[0]

        write_deck_csv(best_deck, self.staging_dir / "deck_new.csv")
        write_deck_report(current_archetype, best_scores, weak_metric, self.staging_dir / "deck_report.json")

        return {"status": "success", "deck_score": best_scores["deck_score"], "archetype": current_archetype}
