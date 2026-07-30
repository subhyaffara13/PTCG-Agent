import json
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

def compute_logic_delta(logs):
    reasoning_logs = logs["reasoning_test"]["reasoning"] or []
    fired = [log for log in reasoning_logs if log.get("reasoning_fired") is True]
    if not fired:
        return 0.0
    return (sum(1 for log in fired if log.get("reasoning_outcome") == "positive") -
            sum(1 for log in fired if log.get("reasoning_outcome") == "negative")) / len(fired)

def check_stalemate(logs):
    rt = logs.get("reasoning_test", {}).get("game_data", {})
    if rt.get("prizes_taken_b", 0) == 0 and rt.get("prizes_taken_a", 0) == 0:
        if rt.get("turns_taken", 0) >= 90:
            logger.error("CRITICAL_STALEMATE_ERROR: reasoning_test match ended in timeout with 0 prizes taken!")
            return True
    return False

def build_eval_report(iteration_result, raw_reasoning, raw_deck, raw_variance, logic_delta, deck_delta, stalemate_detected, eval_state):
    adj_reasoning = max(0.0, raw_reasoning - raw_variance)
    adj_deck = max(0.0, raw_deck - raw_variance)
    is_regression = (raw_reasoning < 0.40) or (logic_delta < -0.20) or stalemate_detected
    flag_deck = eval_state["consecutive_deck_failures"] >= 2
    flag_logic = eval_state["consecutive_logic_failures"] >= 2
    recommendation = "revert_change" if is_regression else ("rebuild_both" if (flag_deck and flag_logic) else ("rebuild_deck" if flag_deck else ("rebuild_logic" if flag_logic else "tune")))
    return {
        "iteration": iteration_result.get("iteration", 0), "timestamp": datetime.now().isoformat(),
        "eval_context": iteration_result.get("eval_context", "default"),
        "raw_scores": {"reasoning_test": round(raw_reasoning, 4), "deck_test": round(raw_deck, 4), "variance_baseline": round(raw_variance, 4)},
        "adjusted_scores": {"reasoning_test": round(adj_reasoning, 4), "deck_test": round(adj_deck, 4)},
        "metrics": {"logic_delta": round(logic_delta, 4), "deck_delta": round(deck_delta, 4), "variance_baseline": round(raw_variance, 4)},
        "consecutive_failures": {"deck": eval_state["consecutive_deck_failures"], "logic": eval_state["consecutive_logic_failures"]},
        "flags": {"flag_deck_architect": flag_deck, "flag_builder_agent": flag_logic, "stalemate_detected": stalemate_detected, "is_regression": is_regression},
        "recommendation": recommendation,
        "version_scores": {"player_a": round(adj_reasoning, 4), "player_b": round(adj_deck, 4), "best_version": "player_b" if (adj_deck > adj_reasoning and not is_regression) else "player_a"}
    }
