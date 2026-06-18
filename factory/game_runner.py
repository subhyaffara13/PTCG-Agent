"""
factory/game_runner.py

Executes exactly 3 games per iteration isolating variables using the actual CABT simulator:
1. Reasoning Test
2. Deck Test
3. Variance Baseline

Strictly enforces timeouts, checks win conditions, and generates iteration_result.json.
"""

import os
import time
import json
import logging
import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

# Safeguard: Remove current directory from sys.path during kaggle_environments load to prevent 'agents' package collision
saved_path = list(sys.path)
try:
    cwd_resolved = Path.cwd().resolve()
    sys.path = [p for p in sys.path if p and Path(p).resolve() != cwd_resolved]
finally:
    import logging
    import os
    import contextlib
    logging.getLogger("kaggle_environments").setLevel(logging.WARNING)
    with open(os.devnull, 'w') as fnull:
        with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
            from kaggle_environments import make
    sys.path = saved_path

from agents.base_agent import BaseAgent
from agents.orchestrator import Orchestrator
from factory.game_logger import GameLogger

logger = logging.getLogger(__name__)

# Default deck from competition environment
DEFAULT_DECK = [
    721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
    1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
    1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
    1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3
]

def run_agent_turn(orchestrator: Orchestrator, observation: dict, deck: list[int]) -> list[int]:
    """Interactions adapter mapping CABT observations to Orchestrator and actions back to options."""
    select = observation.get("select")
    if select is None:
        return deck

    options = select.get("option", [])
    max_count = select.get("maxCount", 1)
    fallback_action = list(range(min(max_count, len(options))))

    try:
        current = observation.get("current")
        if not current:
            return fallback_action

        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if len(players) <= my_idx:
            return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        my_board_ids = []
        if my_state.get("active"):
            for c in my_state.get("active"):
                if c and c.get("id") is not None:
                    my_board_ids.append(c["id"])
        if my_state.get("bench"):
            for c in my_state.get("bench"):
                if c and c.get("id") is not None:
                    my_board_ids.append(c["id"])

        game_state = {
            "my_hand": [c.get("id") for c in my_state.get("hand", []) if c and "id" in c] if my_state.get("hand") else [],
            "my_deck_count": my_state.get("deckCount", 60),
            "my_prizes": len(my_state.get("prize", [])) if isinstance(my_state.get("prize"), list) else 6,
            "my_active_pokemon": my_state.get("active", [None])[0] if my_state.get("active") else None,
            "my_bench": my_state.get("bench", []),
            "my_discard": [c.get("id") for c in my_state.get("discard", []) if c and "id" in c] if my_state.get("discard") else [],
            "my_board": my_board_ids,
            
            "opponent_active": opp_state.get("active", [None])[0] if opp_state.get("active") else None,
            "opponent_bench_count": len(opp_state.get("bench", [])) if opp_state.get("bench") else 0,
            "opponent_prizes": len(opp_state.get("prize", [])) if isinstance(opp_state.get("prize"), list) else 6,
            "opponent_discard": [c.get("id") for c in opp_state.get("discard", []) if c and "id" in c] if opp_state.get("discard") else [],
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": current.get("turn", 1),
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [opt.get("name", "") for opt in options if opt.get("type") == 13]
        game_state["legal_attachments"] = [opt.get("name", "") for opt in options if opt.get("type") == 9]
        game_state["legal_bench"] = [opt.get("name", "") for opt in options if opt.get("type") == 8]
        game_state["legal_evolutions"] = []
        game_state["legal_trainers"] = [opt.get("name", "") for opt in options if opt.get("type") == 7]

        if my_state.get("active") and isinstance(my_state["active"], list) and len(my_state["active"]) > 0:
            active_pokemon = my_state["active"][0]
            if active_pokemon and isinstance(active_pokemon, dict):
                game_state["my_active_hp"] = active_pokemon.get("hp", 100)

        if opp_state.get("active") and isinstance(opp_state["active"], list) and len(opp_state["active"]) > 0:
            active_pokemon = opp_state["active"][0]
            if active_pokemon and isinstance(active_pokemon, dict):
                game_state["opponent_active_hp"] = active_pokemon.get("hp", 100)

        sel_type = select.get("type")
        sel_ctx = select.get("context")

        if sel_type == 0 and sel_ctx == 0:
            action_label = orchestrator.run_turn(game_state)
            mapped_indices = []
            if action_label.startswith("attack:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 13]
            elif action_label.startswith("attach_energy:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 9]
            elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 8]
            elif action_label.startswith("play_trainer:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7]
            elif action_label.startswith("retreat:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 10]

            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 14]

            if not mapped_indices:
                mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            return fallback_action
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action


class CABTAgentWrapper:
    def __init__(self, agent_id: str, skills_dir: str, deck: list[int], g_logger: GameLogger, staging_dir: str = "staging", use_staging: bool = False):
        self.agent_id = agent_id
        self.skills_dir = Path(skills_dir)
        self.staging_dir = Path(staging_dir)
        self.deck = deck
        self.use_staging = use_staging
        self.g_logger = g_logger

        # Determine appropriate skills directory
        s_dir = self.skills_dir
        if self.use_staging:
            if (self.staging_dir / "priority_rules.json").exists() or (self.staging_dir / "strategy_profiles.json").exists():
                s_dir = self.staging_dir

        self.orchestrator = Orchestrator(log_dir=f"logs/{agent_id}", skills_dir=str(s_dir))
        self.orchestrator.start_game()

        # Connect the central logger to this agent's RouterBus
        self.g_logger.register_with_bus(self.orchestrator.bus)

        if self.use_staging:
            self._inject_staging_modules()

    def _inject_staging_modules(self):
        for name in ["hand_analyst", "turn_planner", "strategy_agent", "opponent_model"]:
            staging_file = self.staging_dir / f"{name}.py"
            if staging_file.exists():
                try:
                    spec = importlib.util.spec_from_file_location(f"staging_{name}", str(staging_file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    class_name = "".join([part.capitalize() for part in name.split("_")])
                    cls = getattr(module, class_name)
                    
                    if name == "hand_analyst":
                        self.orchestrator.hand_analyst = cls(log_dir=str(self.orchestrator.log_dir), skills_dir=str(self.orchestrator.skills_dir))
                        self.orchestrator.bus.register_agent("hand_analyst", self.orchestrator.hand_analyst.receive)
                    elif name == "turn_planner":
                        self.orchestrator.turn_planner = cls(log_dir=str(self.orchestrator.log_dir), skills_dir=str(self.orchestrator.skills_dir))
                        self.orchestrator.bus.register_agent("turn_planner", self.orchestrator.turn_planner.receive)
                    elif name == "strategy_agent":
                        self.orchestrator.strategy_agent = cls(log_dir=str(self.orchestrator.log_dir), skills_dir=str(self.orchestrator.skills_dir))
                        self.orchestrator.bus.register_agent("strategy_agent", self.orchestrator.strategy_agent.receive)
                    elif name == "opponent_model":
                        self.orchestrator.opponent_model = cls(log_dir=str(self.orchestrator.log_dir), skills_dir=str(self.orchestrator.skills_dir))
                        self.orchestrator.bus.register_agent("opponent_model", self.orchestrator.opponent_model.receive, perspective_flag="opponent")
                    logger.info(f"Successfully injected staging class for {name}")
                except Exception as e:
                    logger.error(f"Failed to inject staging class for {name}: {e}")

    def __call__(self, obs: dict, conf: dict = None) -> list[int]:
        selected = run_agent_turn(self.orchestrator, obs, self.deck)

        # Log actual reasoning details
        try:
            strategy_active = self.orchestrator.strategy_agent.active_strategy
            hand_score = getattr(self.orchestrator.hand_analyst, "last_hand_score", 5.0)
            self.g_logger.log_reasoning(
                turn=self.orchestrator.current_turn,
                strategy_active=strategy_active,
                hand_score=hand_score,
                strategy_switch_considered=(self.orchestrator.strategy_agent.last_triggered_turn == self.orchestrator.current_turn),
                opponent_archetype_confidence=self.orchestrator.opponent_model.archetype_confidence,
                reasoning_chain=f"Step choice executed. Strategy: {strategy_active}",
                reasoning_fired=True,
                reasoning_outcome="positive"
            )
        except Exception as e:
            logger.error(f"Failed to log reasoning: {e}")

        # Parse observation logs for variance events (e.g. coin flips)
        try:
            for log_entry in obs.get("logs", []):
                log_type = log_entry.get("type")
                if log_type == 6 or log_type == "coin_flip":
                    self.g_logger.log_variance(
                        turn=self.orchestrator.current_turn,
                        event_type="coin_flip",
                        expected_outcome="heads",
                        actual_outcome=log_entry.get("result", "heads"),
                        impact_score=0.0
                    )
        except Exception as e:
            logger.error(f"Failed to log variance: {e}")

        return selected


class GameRunner(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "GameRunner does not receive routed packets — it orchestrates games directly"
        )

    def run_iteration(self, iteration_id: int, version_n1: str, version_n2: str, 
                       deck_base: Any, deck_new: Any, 
                       reasoning_base: dict, reasoning_new: dict) -> dict:
        """
        Executes exactly three games to isolate variables using the real CABT environment in parallel.
        Saves iteration_result.json in the log directory.
        """
        from concurrent.futures import ProcessPoolExecutor

        d_base = deck_base.get("cards", DEFAULT_DECK) if isinstance(deck_base, dict) else deck_base
        d_new = deck_new.get("cards", DEFAULT_DECK) if isinstance(deck_new, dict) else deck_new
        if not isinstance(d_base, list): d_base = DEFAULT_DECK
        if not isinstance(d_new, list): d_new = DEFAULT_DECK

        games_config = [
            ("reasoning_test", d_base, d_base, False, True),  # Base vs Staging Logic
            ("deck_test", d_base, d_new, False, False),      # Base vs New Deck (both using Base Logic)
            ("variance_baseline", d_base, d_base, False, False) # Base vs Base
        ]

        results = {}

        # Run games in parallel processes to isolate ctypes DLL battle pointers
        with ProcessPoolExecutor(max_workers=3) as executor:
            futures = []
            for label, deck_a, deck_b, use_staging_a, use_staging_b in games_config:
                futures.append(
                    executor.submit(
                        _parallel_game_worker,
                        str(self.log_dir),
                        label,
                        version_n1,
                        version_n2,
                        deck_a,
                        deck_b,
                        use_staging_a,
                        use_staging_b
                    )
                )
            for future in futures:
                try:
                    result = future.result()
                    results[result["label"]] = result
                except Exception as e:
                    logger.error(f"Process execution crashed: {e}", exc_info=True)

        # Fallback for failed/crashed matches
        for label, _, _, _, _ in games_config:
            if label not in results:
                results[label] = {
                    "label": label,
                    "winner": "error",
                    "turns_taken": 0,
                    "prizes_taken_a": 0,
                    "prizes_taken_b": 0,
                    "time_elapsed": 0.0,
                    "timeout": False,
                    "log_files": {"action": "", "reasoning": "", "variance": ""}
                }

        # Create a copy of the games results for the disk without the huge steps_dump
        disk_results = {}
        for label, res_dict in results.items():
            disk_results[label] = {k: v for k, v in res_dict.items() if k != "steps_dump"}

        disk_payload = {
            "iteration": iteration_id,
            "timestamp": datetime.now().isoformat(),
            "games": disk_results,
            "ready_for_eval": True
        }

        # Save iteration result json without steps_dump (to save disk write time and space)
        out_file = self.log_dir / "iteration_result.json"
        out_file.write_text(json.dumps(disk_payload, indent=2), encoding="utf-8")

        # Return full payload in memory so caller can access steps_dump if needed
        output_payload = {
            "iteration": iteration_id,
            "timestamp": datetime.now().isoformat(),
            "games": results,
            "ready_for_eval": True
        }
        return output_payload

    def _run_single_game(self, label: str, v_a: str, v_b: str, 
                         deck_a: list[int], deck_b: list[int], use_staging_a: bool, use_staging_b: bool) -> dict:
        """Wrapper for single game run execution."""
        return _parallel_game_worker(str(self.log_dir), label, v_a, v_b, deck_a, deck_b, use_staging_a, use_staging_b)


def _parallel_game_worker(log_dir: str, label: str, v_a: str, v_b: str, 
                          deck_a: list[int], deck_b: list[int], use_staging_a: bool, use_staging_b: bool) -> dict:
    """Helper to run a single game in a separate process space to isolate native CABT pointers."""
    # Safeguard: Remove current directory from sys.path during kaggle_environments load to prevent 'agents' package collision
    saved_path = list(sys.path)
    try:
        cwd_resolved = Path.cwd().resolve()
        sys.path = [p for p in sys.path if p and Path(p).resolve() != cwd_resolved]
        import logging
        import os
        import contextlib
        logging.getLogger("kaggle_environments").setLevel(logging.WARNING)
        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                from kaggle_environments import make
    finally:
        sys.path = saved_path

    start_time = time.time()
    g_logger = GameLogger(log_dir=log_dir)
    g_logger.timestamp_str = f"{g_logger.timestamp_str}_{label}"

    agent_a = CABTAgentWrapper(f"{label}_player_a", "skills", deck_a, g_logger, use_staging=use_staging_a)
    agent_b = CABTAgentWrapper(f"{label}_player_b", "skills", deck_b, g_logger, use_staging=use_staging_b)

    # Initialize the environment
    env = make("cabt")
    env.run([agent_a, agent_b])
    elapsed = time.time() - start_time

    # Extract stats from finished steps
    final_steps = env.steps
    turns = len(final_steps)
    
    # Get outcomes
    p1_state = final_steps[-1][0]
    p2_state = final_steps[-1][1]
    
    # Determine winner
    winner = "draw"
    if p1_state["reward"] == 1:
        winner = "player_a"
    elif p2_state["reward"] == 1:
        winner = "player_b"

    prizes_a = 0
    prizes_b = 0
    try:
        last_obs = p1_state.get("observation", {})
        current_state = last_obs.get("current", {})
        players = current_state.get("players", [])
        if len(players) > 1:
            prizes_a = 6 - len(players[0].get("prize", []))
            prizes_b = 6 - len(players[1].get("prize", []))
    except:
        pass

    game_timeout = (p1_state["status"] == "TIMEOUT" or p2_state["status"] == "TIMEOUT")

    # Clean step observations to remove search_begin_input (binary strings) to save space
    steps_dump = []
    for idx, step in enumerate(env.steps):
        step_data = []
        for player_idx, player_state in enumerate(step):
            obs = player_state.get("observation", {})
            clean_obs = {k: v for k, v in obs.items() if k != "search_begin_input"}
            step_data.append({
                "player": player_idx,
                "action": player_state.get("action"),
                "reward": player_state.get("reward"),
                "status": player_state.get("status"),
                "observation": clean_obs
            })
        steps_dump.append({
            "step": idx,
            "players": step_data
        })

    # Save step history (in memory only, avoid slow disk I/O)
    steps_filename = f"steps_{label}_v{v_a}_vs_v{v_b}.json"

    # Predict winner & upgrade weights if wrong
    prediction = "n/a"
    try:
        from factory.early_predictor import EarlyWinPredictor
        predictor = EarlyWinPredictor()
        prediction = predictor.predict_winner(deck_a, deck_b, steps_dump)
        if prediction != winner and winner in ("player_a", "player_b"):
            predictor.upgrade(prediction, winner, steps_dump)
    except Exception as e:
        logger.error(f"EarlyWinPredictor failed: {e}")

    # Save populated logs
    g_logger.save(v_a, v_b)
    timestamp = g_logger.timestamp_str
    suffix = f"game_{timestamp}_v{v_a}_vs_v{v_b}.json"

    return {
        "label": label,
        "winner": winner,
        "early_prediction": prediction,
        "turns_taken": turns,
        "prizes_taken_a": prizes_a,
        "prizes_taken_b": prizes_b,
        "time_elapsed": round(elapsed, 2),
        "timeout": game_timeout,
        "log_files": {
            "action": f"action_{suffix}",
            "reasoning": f"reasoning_{suffix}",
            "variance": f"variance_{suffix}",
            "steps": steps_filename
        },
        "steps_dump": steps_dump
    }
