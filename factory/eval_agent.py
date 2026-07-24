"""
factory/eval_agent.py
Evaluates the results of the GameRunner iteration by processing game logs.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from cb_agents.base_agent import BaseAgent
from factory.eval_reporter import EvalReporter
from factory.eval_agent_helpers import determine_context, score_game_metrics

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

    _determine_context = staticmethod(determine_context)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("EvalAgent does not receive routed packets")

    def evaluate(self, iteration_result: dict, change_type: str = "default", archetype: str = "default") -> dict:
        eval_context = determine_context(change_type, archetype)
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

        reasoning_logs = logs["reasoning_test"]["reasoning"] or []
        fired = [log for log in reasoning_logs if log.get("reasoning_fired") is True]
        logic_delta = (sum(1 for log in fired if log.get("reasoning_outcome") == "positive") -
                       sum(1 for log in fired if log.get("reasoning_outcome") == "negative")) / len(fired) if fired else 0.0

        raw_reasoning = score_game_metrics(logs["reasoning_test"], weights, logic_delta, self.theoretical_min_turns)
        raw_deck = score_game_metrics(logs["deck_test"], weights, logic_delta, self.theoretical_min_turns)
        raw_variance = score_game_metrics(logs["variance_baseline"], weights, logic_delta, self.theoretical_min_turns)

        adj_reasoning, adj_deck = max(0.0, raw_reasoning - raw_variance), max(0.0, raw_deck - raw_variance)
        deck_delta = adj_deck - adj_reasoning

        stalemate_detected = False
        if logs.get("reasoning_test", {}).get("game_data", {}).get("prizes_taken_b", 0) == 0 and logs.get("reasoning_test", {}).get("game_data", {}).get("prizes_taken_a", 0) == 0:
            if logs.get("reasoning_test", {}).get("game_data", {}).get("turns_taken", 0) >= 90:
                stalemate_detected = True
                logger.error("CRITICAL_STALEMATE_ERROR: reasoning_test match ended in timeout with 0 prizes taken!")
        
        self.eval_state["consecutive_deck_failures"] = self.eval_state["consecutive_deck_failures"] + 1 if deck_delta < 0.1 else 0
        self.eval_state["consecutive_logic_failures"] = self.eval_state["consecutive_logic_failures"] + 1 if logic_delta < 0.1 else 0
        try:
            self.state_file.write_text(json.dumps(self.eval_state, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save evaluation state: {e}")

        flag_deck, flag_logic = self.eval_state["consecutive_deck_failures"] >= 2, self.eval_state["consecutive_logic_failures"] >= 2
        
        # Regression Guard: if raw reasoning drops severely or logic delta is negative, flag revert
        is_regression = (raw_reasoning < 0.40) or (logic_delta < -0.20) or stalemate_detected
        recommendation = "revert_change" if is_regression else ("rebuild_both" if (flag_deck and flag_logic) else ("rebuild_deck" if flag_deck else ("rebuild_logic" if flag_logic else "tune")))
        player_a_score, player_b_score = adj_reasoning, adj_deck

        report = {
            "iteration": iteration_result.get("iteration", 0), "timestamp": datetime.now().isoformat(),
            "eval_context": eval_context,
            "raw_scores": {"reasoning_test": round(raw_reasoning, 4), "deck_test": round(raw_deck, 4), "variance_baseline": round(raw_variance, 4)},
            "adjusted_scores": {"reasoning_test": round(adj_reasoning, 4), "deck_test": round(adj_deck, 4)},
            "metrics": {"logic_delta": round(logic_delta, 4), "deck_delta": round(deck_delta, 4), "variance_baseline": round(raw_variance, 4)},
            "consecutive_failures": {"deck": self.eval_state["consecutive_deck_failures"], "logic": self.eval_state["consecutive_logic_failures"]},
            "flags": {"flag_deck_architect": flag_deck, "flag_builder_agent": flag_logic, "stalemate_detected": stalemate_detected, "is_regression": is_regression},
            "recommendation": recommendation,
            "version_scores": {"player_a": round(player_a_score, 4), "player_b": round(player_b_score, 4), "best_version": "player_b" if (player_b_score > player_a_score and not is_regression) else "player_a"}
        }
        self.reporter.write_report(report)
        return report
