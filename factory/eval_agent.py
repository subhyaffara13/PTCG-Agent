"""
factory/eval_agent.py

Evaluates the results of the GameRunner iteration by processing game logs,
calculating context-aware weighted metrics, checking logic/deck deltas.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
from factory.eval_reporter import EvalReporter

logger = logging.getLogger(__name__)

class EvalAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.reporter = EvalReporter(self.log_dir, self.skills_dir)
        self.rubric = self.reporter.load_rubric()
        self.theoretical_min_turns = self.reporter.load_theoretical_min()
        self.state_file = self.log_dir / "eval_state.json"
        self.eval_state = self.reporter.load_eval_state(self.state_file)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("EvalAgent does not receive routed packets")

    def _determine_context(self, change_type: str, archetype: str) -> str:
        if change_type == "deck_swap": return "deck_test"
        if change_type == "strategy_patch":
            return "aggro_test" if archetype in ("aggro", "control", "combo", "utility") else "meta_test"
        return "micro_patch" if change_type == "micro_patch" else "aggro_test"

    def evaluate(self, iteration_result: dict, change_type: str = "default", archetype: str = "default") -> dict:
        eval_context = self._determine_context(change_type, archetype)
        weights = self.rubric.get("contexts", {}).get(eval_context, {
            "win_rate": 0.35, "prize_efficiency": 0.25, "turn_efficiency": 0.00, "ko_rate": 0.20, "logic_delta": 0.20
        })

        games = iteration_result.get("games", {})
        logs = {}
        for key in ["reasoning_test", "deck_test", "variance_baseline"]:
            game_data = games.get(key, {})
            log_files = game_data.get("log_files", {})
            logs[key] = {
                "action": self.reporter.load_log_file(log_files.get("action")),
                "reasoning": self.reporter.load_log_file(log_files.get("reasoning")),
                "variance": self.reporter.load_log_file(log_files.get("variance")),
                "game_data": game_data
            }

        # Calculate logic delta and score games
        logic_delta = self._calculate_logic_delta(logs["reasoning_test"]["reasoning"])
        raw_reasoning = self._score_game(logs["reasoning_test"], weights, logic_delta)
        raw_deck = self._score_game(logs["deck_test"], weights, logic_delta)
        raw_variance = self._score_game(logs["variance_baseline"], weights, logic_delta)

        # Subtract baseline
        adj_reasoning, adj_deck = max(0.0, raw_reasoning - raw_variance), max(0.0, raw_deck - raw_variance)
        deck_delta = adj_deck - adj_reasoning

        # Update failure states
        self.eval_state["consecutive_deck_failures"] = self.eval_state["consecutive_deck_failures"] + 1 if deck_delta < 0.1 else 0
        self.eval_state["consecutive_logic_failures"] = self.eval_state["consecutive_logic_failures"] + 1 if logic_delta < 0.1 else 0
        try:
            self.state_file.write_text(json.dumps(self.eval_state, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save evaluation state: {e}")

        flag_deck_architect = self.eval_state["consecutive_deck_failures"] >= 2
        flag_builder_agent = self.eval_state["consecutive_logic_failures"] >= 2
        
        recommendation = "rebuild_both" if (flag_deck_architect and flag_builder_agent) else (
            "rebuild_deck" if flag_deck_architect else ("rebuild_logic" if flag_builder_agent else "tune")
        )

        player_a_score, player_b_score = adj_reasoning, adj_deck
        best_version = "player_b" if player_b_score > player_a_score else "player_a"

        report = {
            "iteration": iteration_result.get("iteration", 0), "timestamp": datetime.now().isoformat(),
            "eval_context": eval_context,
            "raw_scores": {"reasoning_test": round(raw_reasoning, 4), "deck_test": round(raw_deck, 4), "variance_baseline": round(raw_variance, 4)},
            "adjusted_scores": {"reasoning_test": round(adj_reasoning, 4), "deck_test": round(adj_deck, 4)},
            "metrics": {"logic_delta": round(logic_delta, 4), "deck_delta": round(deck_delta, 4), "variance_baseline": round(raw_variance, 4)},
            "consecutive_failures": {"deck": self.eval_state["consecutive_deck_failures"], "logic": self.eval_state["consecutive_logic_failures"]},
            "flags": {"flag_deck_architect": flag_deck_architect, "flag_builder_agent": flag_builder_agent},
            "recommendation": recommendation,
            "version_scores": {"player_a": round(player_a_score, 4), "player_b": round(player_b_score, 4), "best_version": best_version}
        }
        self.reporter.write_report(report)
        return report

    def _calculate_logic_delta(self, reasoning_logs: list) -> float:
        if not reasoning_logs: return 0.0
        fired = [log for log in reasoning_logs if log.get("reasoning_fired") is True]
        if not fired: return 0.0
        pos = sum(1 for log in fired if log.get("reasoning_outcome") == "positive")
        neg = sum(1 for log in fired if log.get("reasoning_outcome") == "negative")
        return (pos - neg) / len(fired)

    def _score_game(self, game_logs: dict, weights: dict, logic_delta: float) -> float:
        data = game_logs.get("game_data", {})
        if not data or data.get("winner") == "error": return 0.0

        turns = max(1, data.get("turns_taken", 1))
        win_rate = 1.0 if data.get("winner") == "player_b" else 0.0
        prizes = data.get("prizes_taken_b", 0)
        
        return (
            win_rate * weights.get("win_rate", 0.0) +
            (prizes / turns) * weights.get("prize_efficiency", 0.0) +
            (self.theoretical_min_turns / turns) * weights.get("turn_efficiency", 0.0) +
            (1.0 if prizes > 0 else 0.0) * weights.get("ko_rate", 0.0) +
            logic_delta * weights.get("logic_delta", 0.0)
        )
