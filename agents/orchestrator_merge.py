from agents.orchestrator_types import TurnDecision


def _merge(
    gs, time_result, hand_result, plan_result, strat_result, opp_result,
) -> TurnDecision:
    try:
        final_actions = plan_result.get("action_sequence", ["PASS"])
        if time_result.get("directive", "NORMAL") == "FAST_MOVE":
            final_actions = final_actions[:1] if final_actions else ["PASS"]
        primary_action = final_actions[0] if final_actions else "PASS"
        return TurnDecision(
            timing_directive=time_result.get("directive", "NORMAL"),
            time_remaining=time_result.get("time_remaining", 600.0),
            hand_score=hand_result.get("hand_score", 0.0),
            priority_profile=hand_result.get("priority_profile", "defensive"),
            top_play=hand_result.get("top_play", "PASS"),
            strategy=strat_result.get("strategy", "unknown"),
            posture=strat_result.get("posture", "defensive"),
            strategy_confidence=strat_result.get("confidence", 0.0),
            predicted_opponent_action=opp_result.get("predicted_next_action", "unknown"),
            opponent_archetype=opp_result.get("inferred_deck_type", "unknown"),
            opponent_confidence=opp_result.get("archetype_confidence", 0.0),
            final_actions=final_actions,
            primary_action=primary_action,
        )
    except Exception:
        return _emergency_pass(time_result)


def _emergency_pass(time_result) -> TurnDecision:
    return TurnDecision(
        timing_directive="FORCE_PASS",
        time_remaining=time_result["time_remaining"],
        hand_score=0.0, priority_profile="defensive",
        top_play="(time emergency)", strategy="time_critical",
        posture="defensive", strategy_confidence=1.0,
        predicted_opponent_action="unknown",
        opponent_archetype="unknown", opponent_confidence=0.0,
        final_actions=["PASS"], primary_action="PASS",
    )
