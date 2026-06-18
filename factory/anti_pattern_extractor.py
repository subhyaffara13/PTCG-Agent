import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AntiPatternExtractor:
    """
    Extracts negative behavioral and deck-building patterns from exceptionally poor iterations.
    
    This acts as a meta-learning safeguard. By analyzing games that ended in severe losses
    (e.g., 0 prizes taken or timeouts), it extracts logical constraints ("don'ts") and exports
    them to a configuration file. These constraints are then strictly enforced by the 
    DeckArchitect and StrategyAgent to prevent the system from repeating catastrophic failures.
    """
    def __init__(self, logs_dir: str = "logs", skills_dir: str = "skills"):
        self.logs_dir = Path(logs_dir)
        self.skills_dir = Path(skills_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.donts_file = self.skills_dir / "learned_donts.json"
        
        # Load existing don'ts
        self.learned_donts = self._load_donts()
        
    def _load_donts(self) -> Dict[str, Any]:
        if self.donts_file.exists():
            try:
                return json.loads(self.donts_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {
            "deck_donts": [],
            "behavior_donts": []
        }

    def _save_donts(self):
        try:
            self.donts_file.write_text(json.dumps(self.learned_donts, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save learned don'ts: {e}")

    def analyze_iteration(self, iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], decks: Dict[str, list]):
        """
        Analyzes a single iteration's results to extract anti-patterns.
        Usually called periodically (e.g., every 10 iterations) over historical data,
        but can be called per-iteration.
        """
        # Look for games where our new logic/deck failed miserably (0 prizes taken, timeout, etc)
        for label, game in iteration_result.get("games", {}).items():
            if game.get("winner") == "player_a":  # Assuming player_b is the "new" one we are testing
                prizes_taken_b = game.get("prizes_taken_b", 0)
                timeout = game.get("timeout", False)
                turns = game.get("turns_taken", 0)
                
                # Severe loss threshold
                if prizes_taken_b == 0 or (timeout and prizes_taken_b <= 2) or (turns < 10):
                    logger.info(f"Anti-Pattern Extractor: Analyzing severe loss in {label}")
                    
                    # Analyze the deck that failed
                    deck_b = decks.get("player_b", [])
                    if deck_b:
                        self._extract_deck_anti_patterns(deck_b)
                        
                    # Analyze behavior
                    bv_b = behavioral_vectors.get("player_b")
                    if bv_b:
                        self._extract_behavior_anti_patterns(bv_b)

    def _extract_deck_anti_patterns(self, deck: List[int]):
        """Identifies specific toxic combinations in a bad deck."""
        # Simple heuristic examples
        from agents.card_registry import CardRegistry
        from agents.card_types import CardType
        
        registry = CardRegistry()
        energy_count = 0
        pokemon_count = 0
        trainer_count = 0
        
        for cid in deck:
            c = registry.get(cid)
            if not c: continue
            if c.card_type == CardType.ENERGY: energy_count += 1
            if c.card_type == CardType.POKEMON: pokemon_count += 1
            if c.card_type == CardType.TRAINER: trainer_count += 1
            
        # Example Don't: Too much energy, no trainers
        if energy_count > 25 and trainer_count < 10:
            rule = {"condition": "energy_gt_25_trainer_lt_10", "description": "Deck has >25 energy but <10 trainers (dead draws)."}
            if rule not in self.learned_donts["deck_donts"]:
                self.learned_donts["deck_donts"].append(rule)
                self._save_donts()
                logger.info(f"Extracted deck anti-pattern: {rule['description']}")
                
        # Example Don't: Too many pokemon
        if pokemon_count > 30:
            rule = {"condition": "pokemon_gt_30", "description": "Deck has >30 pokemon, clogs hand."}
            if rule not in self.learned_donts["deck_donts"]:
                self.learned_donts["deck_donts"].append(rule)
                self._save_donts()
                logger.info(f"Extracted deck anti-pattern: {rule['description']}")

    def _extract_behavior_anti_patterns(self, bv: Any):
        """Identifies bad behavioral thresholds."""
        # Expecting BehavioralVector object
        
        if bv.setup_duration > 15:
            rule = {"condition": "setup_duration_gt_15", "description": "Strategy taking >15 turns to attack is a losing pattern."}
            if rule not in self.learned_donts["behavior_donts"]:
                self.learned_donts["behavior_donts"].append(rule)
                self._save_donts()
                logger.info(f"Extracted behavior anti-pattern: {rule['description']}")
                
        if bv.energy_accel_rate < 0.2 and bv.turn_aggro > 0.5:
            rule = {"condition": "high_aggro_low_accel", "description": "Aggro profile without energy acceleration fails."}
            if rule not in self.learned_donts["behavior_donts"]:
                self.learned_donts["behavior_donts"].append(rule)
                self._save_donts()
                logger.info(f"Extracted behavior anti-pattern: {rule['description']}")
