import json
import logging
import random
from pathlib import Path
from factory.game_runner import GameRunner
from agents.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("gauntlet_evaluator")

class GauntletRunner:
    def __init__(self):
        self.archetypes = ["Aggro", "Control", "Setup", "Stall"]
        
    def _generate_generic_deck(self, archetype: str) -> list:
        """Generates a generic dummy deck of the specified archetype to test against."""
        deck = []
        # Fallback simplistic deck generator for gauntlet tests (must use integer IDs)
        for i in range(12):
            deck.append(1) # Basic Pokemon
        for i in range(10):
            deck.append(100) # Trainer
        for i in range(38):
            deck.append(200) # Energy
        return deck

    def run_gauntlet(self, candidate_deck: list, num_games_per_archetype: int = 3) -> bool:
        """
        Runs vnew against multiple archetypes. 
        Returns True if vnew achieves > 50% win rate across the entire Gauntlet.
        """
        logger.info(f"Starting Gauntlet Evaluation against {len(self.archetypes)} archetypes...")
        total_wins = 0
        total_games = len(self.archetypes) * num_games_per_archetype
        runner = GameRunner()
        
        for archetype in self.archetypes:
            logger.info(f"Evaluating against {archetype}...")
            opp_deck = self._generate_generic_deck(archetype)
            
            archetype_wins = 0
            for i in range(num_games_per_archetype):
                res = runner.run_iteration(
                    iteration_id=9999,
                    version_n1="candidate",
                    version_n2=f"gauntlet_{archetype}",
                    deck_base=candidate_deck,
                    deck_new=opp_deck,
                    reasoning_base={},
                    reasoning_new={}
                )
                
                # Check if candidate won
                games = res.get("games", {})
                for label, game in games.items():
                    if game.get("winner") == "player_a": # candidate is player_a
                        total_wins += 1
                        archetype_wins += 1
                
            logger.info(f"Stage Result vs {archetype}: {archetype_wins}/{num_games_per_archetype} wins.")
            
        win_rate = total_wins / total_games
        logger.info(f"Gauntlet Complete. Overall Win Rate: {win_rate*100:.1f}%")
        
        return win_rate >= 0.51

if __name__ == "__main__":
    runner = GauntletRunner()
    # Dummy run
    runner.run_gauntlet([], 1)
