import json
import logging
import random
from pathlib import Path
from factory.game_runner import GameRunner
from cb_agents.orchestrator import Orchestrator
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
        """Loads a realistic, competitive deck for the gauntlet opponent from skills/league/ or card pool."""
        arch_lower = archetype.lower()
        arch_map = {"setup": "combo", "stall": "control"}
        file_key = arch_map.get(arch_lower, arch_lower)
        league_file = self.skills_dir / f"league/{file_key}_exploiter.csv"
        if league_file.exists():
            import csv
            try:
                deck = []
                with open(league_file, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        deck.extend([int(row["card_id"])] * int(row["count"]))
                if len(deck) == 60:
                    logger.info(f"Loaded real competitor deck from {league_file.name} for Gauntlet.")
                    return deck
            except Exception as e:
                logger.warning(f"Failed to load {league_file.name}: {e}")

        # Fallback to generator if league CSV is missing
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
            from factory.game_runner import DEFAULT_DECK
            return list(DEFAULT_DECK)

    def run_gauntlet(self, target_deck: list, num_games_per_stage: int = 2) -> dict:
        """
        Runs target_deck directly against multiple real competitor archetypes in parallel. 
        Returns True if target_deck achieves >= 50% win rate across the entire Gauntlet.
        """
        from factory.game_runner_worker import _parallel_game_worker
        from concurrent.futures import ProcessPoolExecutor
        from factory.game_runner import DEFAULT_DECK

        if not target_deck or not isinstance(target_deck, list) or len(target_deck) != 60:
            target_deck = list(DEFAULT_DECK)
        target_deck = [int(c) for c in target_deck]

        logger.info(f"Starting Gauntlet Evaluation against {len(self.archetypes)} real archetypes...")
        total_wins = 0
        total_games = 0

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        for archetype in self.archetypes:
            logger.info(f"Evaluating against {archetype}...")
            opp_deck = self._generate_real_deck(archetype)
            opp_deck = [int(c) for c in opp_deck]

            archetype_wins = 0
            archetype_games = 0

            futures = []
            with ProcessPoolExecutor(max_workers=min(8, num_games_per_stage * 2)) as executor:
                for i in range(num_games_per_stage):
                    seed_orig = 5000 + i * 2
                    seed_swap = 5001 + i * 2

                    # Orig: Candidate (player_a) vs Competitor (player_b)
                    futures.append((
                        executor.submit(
                            _parallel_game_worker, 
                            str(log_dir), f"gauntlet_{archetype}_orig_{i}", 
                            "candidate", f"gauntlet_{archetype}", 
                            target_deck, opp_deck, 
                            False, False, seed_orig, "", ""
                        ),
                        "player_a"
                    ))

                    # Swap: Competitor (player_a) vs Candidate (player_b)
                    futures.append((
                        executor.submit(
                            _parallel_game_worker, 
                            str(log_dir), f"gauntlet_{archetype}_swap_{i}", 
                            f"gauntlet_{archetype}", "candidate", 
                            opp_deck, target_deck, 
                            False, False, seed_swap, "", ""
                        ),
                        "player_b"
                    ))

                for fut, target_player in futures:
                    try:
                        res = fut.result(timeout=600.0)
                        archetype_games += 1
                        total_games += 1
                        if res.get("winner") == target_player:
                            archetype_wins += 1
                            total_wins += 1
                    except Exception as e:
                        logger.error(f"Gauntlet match failed/timed out: {e}")
                        archetype_games += 1
                        total_games += 1

            logger.info(f"Stage Result vs {archetype}: {archetype_wins} wins out of {archetype_games} games played.")

        win_rate = total_wins / max(total_games, 1)
        passed = win_rate >= 0.50
        logger.info(f"Gauntlet Complete. Overall Win Rate: {win_rate*100:.1f}% ({total_wins}/{total_games} wins) - Passed: {passed}")

        return {
            "passed": passed,
            "win_rate": win_rate,
            "total_wins": total_wins,
            "total_games": total_games
        }


if __name__ == "__main__":
    runner = GauntletRunner()
    runner.run_gauntlet([], 1)
