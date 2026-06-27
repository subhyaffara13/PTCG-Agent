import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

from factory.anti_pattern_logger import load_donts, save_donts, run_replays_analysis
from factory.anti_pattern_extractor_helpers import extract_deck_anti_patterns, extract_behavior_anti_patterns

class AntiPatternExtractor:
    """
    Extracts negative behavioral and deck-building patterns from exceptionally poor iterations.
    """
    def __init__(self, logs_dir: str = "logs", skills_dir: str = "skills"):
        self.logs_dir = Path(logs_dir)
        self.skills_dir = Path(skills_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.donts_file = self.skills_dir / "learned_donts.json"
        self.learned_donts = load_donts(self.donts_file)
        
    def _save_donts(self):
        save_donts(self.donts_file, self.learned_donts)

    def analyze_iteration(self, iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], decks: Dict[str, list]):
        """Analyzes a single iteration's results to extract anti-patterns."""
        for label, game in iteration_result.get("games", {}).items():
            if game.get("winner") == "player_a":  # Assuming player_b is the "new" one we are testing
                prizes_taken_b = game.get("prizes_taken_b", 0)
                timeout = game.get("timeout", False)
                turns = game.get("turns_taken", 0)
                
                # Severe loss threshold
                if prizes_taken_b == 0 or (timeout and prizes_taken_b <= 2) or (turns < 10):
                    logger.info(f"Severe loss in {label}. Extracting anti-patterns.")
                    deck_b = decks.get("player_b", [])
                    if deck_b:
                        extract_deck_anti_patterns(deck_b, self.learned_donts, self._save_donts)
                        
                    bv_b = behavioral_vectors.get("player_b")
                    if bv_b:
                        extract_behavior_anti_patterns(bv_b, self.learned_donts, self._save_donts)

    def analyze_losing_replays(self, replay_paths: List[Path], player_name_or_id: str):
        """Analyzes replays to extract anti-patterns."""
        run_replays_analysis(replay_paths, player_name_or_id, self)
