import json
import logging
import random
from pathlib import Path
from factory.game_runner import GameRunner
from agents.orchestrator import Orchestrator
from factory.deck_loader import DeckLoader
from factory.deck_generator import DeckGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("gauntlet_evaluator")


class GauntletRunner:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.archetypes = ["Aggro", "Control", "Setup", "Stall"]
        
        # Load card metadata dynamically to generate real competitor decks
        loader = DeckLoader(self.skills_dir)
        self.card_pool = loader.load_card_pool()
        self.archetypes_data = loader.load_archetypes_data()
        self.card_details = loader.parse_card_details(self.card_pool)
        self.generator = DeckGenerator(self.card_pool, self.card_details, self.archetypes_data)

    def _generate_real_deck(self, archetype: str) -> list:
        """Generates a realistic, competitive deck for the gauntlet opponent."""
        arch_lower = archetype.lower()
        # Fallback to combo if archetype is setup or stall
        if arch_lower not in self.archetypes_data.get("archetypes", {}):
            arch_lower = "combo"
            
        legal = [c for c in self.card_pool if c.get("archetype") == arch_lower or c.get("card_type") == "Energy"]
        basics = [c for c in self.card_pool if c.get("card_type") == "Pokemon" 
                  and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"]
        energies = [c for c in self.card_pool if c.get("card_type") == "Energy"]
        
        try:
            cand = self.generator.generate_candidate(legal, basics, energies, arch_lower)
            return [int(c["card_id"]) for c in cand]
        except Exception as e:
            logger.warning(f"Failed to generate real deck for {archetype}: {e}. Falling back to default.")
            return [1]*12 + [100]*10 + [200]*38

    def run_gauntlet(self, candidate_deck: list, num_games_per_archetype: int = 3) -> bool:
        """
        Runs candidate_deck against multiple real archetypes. 
        Returns True if candidate_deck achieves > 50% win rate across the entire Gauntlet.
        """
        logger.info(f"Starting Gauntlet Evaluation against {len(self.archetypes)} real archetypes...")
        total_wins = 0
        total_games = 0
        runner = GameRunner()
        
        for archetype in self.archetypes:
            logger.info(f"Evaluating against {archetype}...")
            opp_deck = self._generate_real_deck(archetype)
            
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
                total_games += len(games)
                for label, game in games.items():
                    if game.get("winner") == "player_a":
                        total_wins += 1
                        archetype_wins += 1
                
            logger.info(f"Stage Result vs {archetype}: {archetype_wins} wins out of {num_games_per_archetype * 61} games played.")
            
        win_rate = total_wins / max(total_games, 1)
        logger.info(f"Gauntlet Complete. Overall Win Rate: {win_rate*100:.1f}% ({total_wins}/{total_games} wins)")
        
        return win_rate


if __name__ == "__main__":
    runner = GauntletRunner()
    runner.run_gauntlet([], 1)
