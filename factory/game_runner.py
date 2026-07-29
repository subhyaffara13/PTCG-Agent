"""
factory/game_runner.py
Runs parallel game playouts for iteration evaluations.
"""
import os
import time
import json
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from cb_agents.base_agent import BaseAgent
from factory.game_runner_worker import _parallel_game_worker


def _mutate_deck(deck: list[int], mutation_rate: float = 0.30) -> list[int]:
    if len(deck) != 60:
        return deck
    if random.random() > mutation_rate:
        return deck
    d = list(deck)
    pool = list(set(deck))
    n_changes = random.randint(2, 5)
    for _ in range(n_changes):
        i = random.randrange(60)
        d[i] = random.choice(pool)
    return d

logger = logging.getLogger(__name__)

def _load_optimized_deck(custom_path: str | None = None) -> list[int]:
    """Load the best deck from the optimizer pipeline output."""
    import csv
    paths = [custom_path] if custom_path else ["submission/deck.csv", "staging/deck_new.csv", "cb_agents/deck_new.csv", "deck.csv"]
    for deck_path in paths:
        p = Path(deck_path)
        if p.exists():
            try:
                deck = []
                with open(p, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        deck.extend([int(row["card_id"])] * int(row["count"]))
                if len(deck) == 60:
                    logger.info("Loaded optimized deck from %s (%d cards)", deck_path, len(deck))
                    return deck
            except Exception as e:
                logger.warning("Failed to load deck from %s: %s", deck_path, e)
    logger.warning("No optimized deck found, using fallback")
    return [957]*3 + [979]*3 + [37]*3 + [210]*3 + [1121]*1 + [1227]*4 + [1152]*4 + [1210]*3 + [1194]*3 + [1198]*1 + [1229]*1 + [1134]*1 + [1097]*4 + [1182]*4 + [1102]*1 + [1086]*4 + [1123]*1 + [1081]*1 + [1122]*1 + [6]*8 + [4]*6


DEFAULT_DECK = _load_optimized_deck()


class GameRunner(BaseAgent):
    _executor = None

    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        if GameRunner._executor is None:
            import os
            os.environ["OPENBLAS_NUM_THREADS"] = "1"
            os.environ["OMP_NUM_THREADS"] = "1"
            os.environ["MKL_NUM_THREADS"] = "1"
            max_w = min(2, os.cpu_count() or 2)
            GameRunner._executor = ProcessPoolExecutor(max_workers=max_w)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("GameRunner does not receive routed packets")

    def run_iteration(self, iteration_id: int, version_n1: str, version_n2: str, 
                       deck_base: Any, deck_new: Any, 
                       reasoning_base: dict, reasoning_new: dict,
                       num_matchups: int = 10) -> dict:
        d_base = deck_base.get("cards", DEFAULT_DECK) if isinstance(deck_base, dict) else deck_base
        d_new = deck_new.get("cards", DEFAULT_DECK) if isinstance(deck_new, dict) else deck_new
        if not isinstance(d_base, list): d_base = DEFAULT_DECK
        if not isinstance(d_new, list): d_new = DEFAULT_DECK

        # 1. Initialize League Manager & Gauntlet Runner
        from factory.league_manager import LeagueManager
        from factory.gauntlet_runner import GauntletRunner
        league = LeagueManager()
        gauntlet = GauntletRunner(str(self.log_dir.parent / "skills"))

        # RUN GAUNTLET ITERATION: 9 Total Games (1 Reasoning + 4 Archetype Twin Pairs)
        games_config: list[tuple[str, list[int], list[int], bool, bool, int | None, str | None, str | None]] = [
            ("reasoning_test", d_base, d_base, False, True, None, None, None)
        ]
        league_matchups = {}

        # 4 Core Meta-Archetypes: Aggro (Lightning), Water (Baxcalibur), Fire (Charizard), Control (Pidgeot)
        core_archetypes = ["Aggro", "Control", "Setup", "Stall"]
        mutated_new = _mutate_deck(d_new)

        for idx, arch in enumerate(core_archetypes):
            seed = 2000 + idx
            opp_deck = gauntlet._generate_real_deck(arch)
            opp_name = f"gauntlet_{arch}"
            
            # Record matchup for Elo tracking
            league_matchups[f"deck_test_{idx}_orig"] = opp_name
            league_matchups[f"deck_test_{idx}_swap"] = opp_name
            
            # Symmetric Twin Pair against Real League Archetype
            games_config.extend([
                (f"deck_test_{idx}_orig", opp_deck, mutated_new, False, False, seed, None, None),
                (f"deck_test_{idx}_swap", mutated_new, opp_deck, False, False, seed, None, None)
            ])

        results = {}
        executor = GameRunner._executor
        if executor is None:
            GameRunner._executor = ProcessPoolExecutor(max_workers=os.cpu_count() or 16)
            executor = GameRunner._executor
        assert executor is not None

        try:
            futures = [
                executor.submit(_parallel_game_worker, str(self.log_dir), label, version_n1, version_n2, deck_a, deck_b, use_a, use_b, seed, model_path_a or "", model_path_b or "")
                for label, deck_a, deck_b, use_a, use_b, seed, model_path_a, model_path_b in games_config
            ]
        except RuntimeError as re:
            if "after shutdown" in str(re):
                logger.warning("GameRunner executor was previously shut down. Re-initializing new ProcessPoolExecutor...")
                GameRunner._executor = ProcessPoolExecutor(max_workers=os.cpu_count() or 16)
                executor = GameRunner._executor
                futures = [
                    executor.submit(_parallel_game_worker, str(self.log_dir), label, version_n1, version_n2, deck_a, deck_b, use_a, use_b, seed, model_path_a or "", model_path_b or "")
                    for label, deck_a, deck_b, use_a, use_b, seed, model_path_a, model_path_b in games_config
                ]
            else:
                raise
        for future in futures:
            try:
                # Enforce a 330s max timeout per evaluation game future to exceed the 300s Kaggle engine timeout
                res = future.result(timeout=330.0)
                results[res["label"]] = res
            except Exception as e:
                logger.error(f"Process execution crashed or timed out: {e}")
                # Reset executor on timeout or pool breakage so hung child processes are killed and recreated cleanly
                logger.warning("Resetting GameRunner worker pool to clear hung processes...")
                try:
                    if GameRunner._executor:
                        GameRunner._executor.shutdown(wait=False, cancel_futures=True)
                except Exception:
                    pass
                GameRunner._executor = None

        # Normalize swapped twin games:
        # In swap configurations, deck_a was d_new and deck_b was opponent_deck.
        # We swap the metrics back so player_a represents the baseline opponent and player_b represents d_new
        for label, res in list(results.items()):
            if label.endswith("_swap"):
                orig_winner = res.get("winner")
                if orig_winner == "player_a":
                    res["winner"] = "player_b"
                elif orig_winner == "player_b":
                    res["winner"] = "player_a"
                
                pa = res.get("prizes_taken_a", 0)
                pb = res.get("prizes_taken_b", 0)
                res["prizes_taken_a"] = pb
                res["prizes_taken_b"] = pa

        # Update League ELO based on matchmaking results
        for label, opp_name in league_matchups.items():
            res = results.get(label)
            if res and res.get("winner") != "error":
                winner = res.get("winner") # "player_a" (opp won), "player_b" (new agent won), or "draw"
                league.update_elo(opp_name, "main_agent", winner)
                if opp_name.startswith("checkpoint_"):
                    try:
                        from factory.model_checkpoint_manager import ModelCheckpointManager
                        mcm = ModelCheckpointManager()
                        result = 1.0 if winner == "player_a" else (0.0 if winner == "player_b" else 0.5)
                        opponent_elo = league.ratings.get("main_agent", 1200.0)
                        mcm.update_checkpoint_elo(opp_name, opponent_elo, result)
                    except Exception as e:
                        logger.debug(f"Failed to update checkpoint Elo: {e}")

        # Consolidate results for EvalAgent (average metrics across all parallel runs)
        for prefix, key in [("deck_test", "deck_test"), ("variance_baseline", "variance_baseline")]:
            workers = [res for k, res in results.items() if k.startswith(prefix)]
            if workers:
                win_counts = Counter(w.get("winner") for w in workers)
                results[key] = {
                    "label": key, "winner": win_counts.most_common(1)[0][0],
                    "turns_taken": int(sum(w.get("turns_taken", 0) for w in workers) / len(workers)),
                    "prizes_taken_a": int(sum(w.get("prizes_taken_a", 0) for w in workers) / len(workers)),
                    "prizes_taken_b": int(sum(w.get("prizes_taken_b", 0) for w in workers) / len(workers)),
                    "time_elapsed": workers[0].get("time_elapsed", 0.0),
                    "timeout": any(w.get("timeout") for w in workers),
                    "log_files": workers[0].get("log_files", {})
                }

        # Ensure fallback keys
        for k in ["reasoning_test", "deck_test", "variance_baseline"]:
            if k not in results:
                results[k] = {"winner": "error", "turns_taken": 0, "log_files": {}}

        disk_results = {label: {k: v for k, v in res.items() if k != "steps_dump"} for label, res in results.items()}
        disk_payload = {
            "iteration": iteration_id, "timestamp": datetime.now().isoformat(),
            "games": disk_results, "ready_for_eval": True
        }
        (self.log_dir / "iteration_result.json").write_text(json.dumps(disk_payload, indent=2), encoding="utf-8")

        return {"iteration": iteration_id, "timestamp": datetime.now().isoformat(), "games": results, "ready_for_eval": True}
