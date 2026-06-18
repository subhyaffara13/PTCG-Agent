"""
factory/eval_agent.py

Evaluates the results of the GameRunner iteration by processing game logs,
calculating context-aware weighted metrics, checking logic/deck deltas,
and outputs logs/eval_report.json and logs/eval_state.json.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class EvalAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Load eval_rubric.json once on init only
        self.rubric = self._load_rubric()
        
        # Load theoretical_min defaults from deck_rubric.json
        self.theoretical_min_turns = self._load_theoretical_min()

        # Load consecutive failures persistence on init
        self.state_file = self.log_dir / "eval_state.json"
        self.eval_state = self._load_eval_state()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "EvalAgent does not receive routed packets — it scores iterations directly"
        )

    def _load_eval_state(self) -> dict:
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                return {
                    "consecutive_deck_failures": data.get("consecutive_deck_failures", 0),
                    "consecutive_logic_failures": data.get("consecutive_logic_failures", 0)
                }
            except Exception:
                pass
        return {"consecutive_deck_failures": 0, "consecutive_logic_failures": 0}

    def _load_rubric(self) -> dict:
        path = self.skills_dir / "eval_rubric.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load evaluation rubric: {e}")
            return {"contexts": {}}

    def _load_theoretical_min(self) -> int:
        path = self.skills_dir / "deck_rubric.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("theoretical_min_turns", 4)
        except Exception:
            return 4

    def _determine_context(self, change_type: str, archetype: str) -> str:
        if change_type == "deck_swap":
            return "deck_test"
        elif change_type == "strategy_patch":
            if archetype in ("aggro", "control", "combo", "utility"):
                return "aggro_test" # matching context patterns in eval_rubric.json
            return "meta_test"
        elif change_type == "micro_patch":
            return "micro_patch"
        return "aggro_test"

    def evaluate(self, iteration_result: dict, change_type: str = "default", archetype: str = "default") -> dict:
        """
        Ingests the results of 3 simulation games, calculates deltas, persists failure counts,
        and outputs eval_report.json.
        """
        eval_context = self._determine_context(change_type, archetype)
        weights = self.rubric.get("contexts", {}).get(eval_context, {
            "win_rate": 0.35, "prize_efficiency": 0.25, "turn_efficiency": 0.00, "ko_rate": 0.20, "logic_delta": 0.20
        })

        games = iteration_result.get("games", {})
        
        # Load and parse logs
        logs = {}
        for key in ["reasoning_test", "deck_test", "variance_baseline"]:
            game_data = games.get(key, {})
            log_files = game_data.get("log_files", {})
            logs[key] = {
                "action": self._load_log_file(log_files.get("action")),
                "reasoning": self._load_log_file(log_files.get("reasoning")),
                "variance": self._load_log_file(log_files.get("variance")),
                "game_data": game_data
            }

        # Step 2: Compute logic_delta (correlation of reasoning_fired to reasoning_outcome="positive")
        # Logic delta represents difference between Game 1 and Base
        logic_delta = self._calculate_logic_delta(logs["reasoning_test"]["reasoning"])

        # Step 3: Score each game based on context weights
        raw_reasoning = self._score_game(logs["reasoning_test"], weights, logic_delta)
        raw_deck = self._score_game(logs["deck_test"], weights, logic_delta)
        raw_variance = self._score_game(logs["variance_baseline"], weights, logic_delta)

        # Step 5: Subtract variance baseline
        adj_reasoning = max(0.0, raw_reasoning - raw_variance)
        adj_deck = max(0.0, raw_deck - raw_variance)

        # Deck delta = version_score(deck_test) - version_score(reasoning_test)
        deck_delta = adj_deck - adj_reasoning

        # Step 6: Persist states
        if deck_delta < 0.1:
            self.eval_state["consecutive_deck_failures"] += 1
        else:
            self.eval_state["consecutive_deck_failures"] = 0

        if logic_delta < 0.1:
            self.eval_state["consecutive_logic_failures"] += 1
        else:
            self.eval_state["consecutive_logic_failures"] = 0

        try:
            self.state_file.write_text(json.dumps(self.eval_state, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save evaluation state: {e}")

        flag_deck_architect = self.eval_state["consecutive_deck_failures"] >= 2
        flag_builder_agent = self.eval_state["consecutive_logic_failures"] >= 2

        # Recommendation selection
        if flag_deck_architect and flag_builder_agent:
            recommendation = "rebuild_both"
        elif flag_deck_architect:
            recommendation = "rebuild_deck"
        elif flag_builder_agent:
            recommendation = "rebuild_logic"
        else:
            recommendation = "tune"

        player_a_score = adj_reasoning
        player_b_score = adj_deck
        best_version = "player_b" if player_b_score > player_a_score else "player_a"

        report = {
            "iteration": iteration_result.get("iteration", 0),
            "timestamp": datetime.now().isoformat(),
            "eval_context": eval_context,
            "raw_scores": {
                "reasoning_test": round(raw_reasoning, 4),
                "deck_test": round(raw_deck, 4),
                "variance_baseline": round(raw_variance, 4)
            },
            "adjusted_scores": {
                "reasoning_test": round(adj_reasoning, 4),
                "deck_test": round(adj_deck, 4)
            },
            "metrics": {
                "logic_delta": round(logic_delta, 4),
                "deck_delta": round(deck_delta, 4),
                "variance_baseline": round(raw_variance, 4)
            },
            "consecutive_failures": {
                "deck": self.eval_state["consecutive_deck_failures"],
                "logic": self.eval_state["consecutive_logic_failures"]
            },
            "flags": {
                "flag_deck_architect": flag_deck_architect,
                "flag_builder_agent": flag_builder_agent
            },
            "recommendation": recommendation,
            "version_scores": {
                "player_a": round(player_a_score, 4),
                "player_b": round(player_b_score, 4),
                "best_version": best_version
            }
        }

        # Write eval_report.json
        report_file = self.log_dir / "eval_report.json"
        report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    def _load_log_file(self, filename: str) -> list:
        if not filename:
            return []
        path = self.log_dir / filename
        if not path.exists():
            logger.warning(f"Expected log file not found: {path}")
            return []
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Error reading log file {path}: {e}")
            return []

    def _calculate_logic_delta(self, reasoning_logs: list) -> float:
        if not reasoning_logs:
            return 0.0
        
        fired_turns = [log for log in reasoning_logs if log.get("reasoning_fired") is True]
        if not fired_turns:
            return 0.0

        positive_count = sum(1 for log in fired_turns if log.get("reasoning_outcome") == "positive")
        negative_count = sum(1 for log in fired_turns if log.get("reasoning_outcome") == "negative")
        total = len(fired_turns)

        # logic effectiveness representation between -1.0 and 1.0
        return (positive_count - negative_count) / total

    def _score_game(self, game_logs: dict, weights: dict, logic_delta: float) -> float:
        data = game_logs.get("game_data", {})
        if not data or data.get("winner") == "error":
            return 0.0

        turns = max(1, data.get("turns_taken", 1))
        # Player A or Player B winner check depending on perspective
        win_rate = 1.0 if data.get("winner") == "player_b" else 0.0
        
        prizes = data.get("prizes_taken_b", 0) # evaluating player_b (the candidate)
        prize_efficiency = prizes / turns

        # Turn efficiency: theoretical_min / actual turns
        actual_turns = turns
        turn_efficiency = self.theoretical_min_turns / actual_turns

        # KO rate: ko count / total prizes taken (assuming 1 prize per KO for baseline)
        ko_rate = 1.0 if prizes > 0 else 0.0

        # Version score summation
        score = (
            win_rate * weights.get("win_rate", 0.0) +
            prize_efficiency * weights.get("prize_efficiency", 0.0) +
            turn_efficiency * weights.get("turn_efficiency", 0.0) +
            ko_rate * weights.get("ko_rate", 0.0) +
            logic_delta * weights.get("logic_delta", 0.0)
        )
        return score
