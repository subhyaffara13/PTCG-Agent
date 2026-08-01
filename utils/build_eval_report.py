
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

