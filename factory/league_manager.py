import json
import logging
from typing import Dict, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class LeagueManager:
    """
    Manages the AlphaStar-style League of Agents.
    Maintains Elo ratings and matchmakes the Main Agent against Exploiters
    to prevent strategy collapse and ensure robust generalization.
    """
    def __init__(self, league_dir: str = "skills/league"):
        self.league_dir = Path(league_dir)
        self.league_dir.mkdir(parents=True, exist_ok=True)
        self.elo_file = self.league_dir / "elo_ratings.json"
        
        self.ratings = self._load_ratings()
        
        # Initialize default league members if empty
        if not self.ratings:
            self.ratings = {
                "main_agent": 1200,
                "main_exploiter": 1200,
                "aggro_exploiter": 1200,
                "control_exploiter": 1200,
                "combo_exploiter": 1200
            }
            self._save_ratings()

    def _load_ratings(self) -> Dict[str, float]:
        if self.elo_file.exists():
            try:
                return json.loads(self.elo_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to load Elo ratings: {e}")
        return {}

    def _save_ratings(self):
        try:
            self.elo_file.write_text(json.dumps(self.ratings, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save Elo ratings: {e}")

    def update_elo(self, agent_a: str, agent_b: str, winner: str, k_factor: int = 32):
        """
        Updates Elo ratings based on match outcome.
        winner: 'player_a', 'player_b', or 'draw'
        """
        r_a = self.ratings.get(agent_a, 1200)
        r_b = self.ratings.get(agent_b, 1200)
        
        expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
        expected_b = 1 / (1 + 10 ** ((r_a - r_b) / 400))
        
        score_a = 0.5
        score_b = 0.5
        if winner == "player_a":
            score_a, score_b = 1.0, 0.0
        elif winner == "player_b":
            score_a, score_b = 0.0, 1.0
            
        self.ratings[agent_a] = r_a + k_factor * (score_a - expected_a)
        self.ratings[agent_b] = r_b + k_factor * (score_b - expected_b)
        
        self._save_ratings()

    def matchmake(self, active_agent: str = "main_agent") -> str:
        """
        Selects an opponent for the active agent to play against next.
        Follows the AlphaStar matchmaking probability:
        - 50% chance to play another Main Agent (past snapshot)
        - 25% chance to play the Main Exploiter
        - 25% chance to play an Archetype Exploiter (Aggro/Control/Combo)
        """
        import random
        r = random.random()
        
        if r < 0.50:
            return "main_agent_snapshot"
        elif r < 0.75:
            return "main_exploiter"
        else:
            exploiters = ["aggro_exploiter", "control_exploiter", "combo_exploiter"]
            # Weight toward the exploiter with the highest Elo
            weights = [self.ratings.get(e, 1200) for e in exploiters]
            return random.choices(exploiters, weights=weights, k=1)[0]
