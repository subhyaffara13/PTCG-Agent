from cb_agents.orchestrator_types import TurnDecision


def _merge(
    gs, time_result, hand_result, plan_result, strat_result, opp_result,
) -> TurnDecision:
    if strat_result["confidence"] >= 0.75:
        final_actions = strat_result["actions"]
    else:
        final_actions = [s["action"] for s in plan_result if s.get("viable", False)]
    if time_result["directive"] == "FAST_MOVE":
        final_actions = final_actions[:1] if final_actions else ["PASS"]
    primary_action = final_actions[0] if final_actions else "PASS"
    return TurnDecision(
        timing_directive=time_result["directive"],
        time_remaining=time_result["time_remaining"],
        hand_score=hand_result["hand_score"],
        priority_profile=hand_result["priority_profile"],
        top_play=hand_result["top_play"],
        strategy=strat_result["strategy"],
        posture=strat_result["posture"],
        strategy_confidence=strat_result["confidence"],
        predicted_opponent_action=opp_result["predicted_next_action"],
        opponent_archetype=opp_result["inferred_deck_type"],
        opponent_confidence=opp_result["archetype_confidence"],
        final_actions=final_actions,
        primary_action=primary_action,
    )


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
