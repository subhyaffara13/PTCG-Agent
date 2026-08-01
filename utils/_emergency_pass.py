
def _emergency_pass(time_result) -> TurnDecision:
    return TurnDecision(
        timing_directive="FORCE_PASS",
        time_remaining=time_result.get("time_remaining", 0.0) if isinstance(time_result, dict) else 0.0,
        hand_score=0.0, priority_profile="defensive",
        top_play="(time emergency)", strategy="time_critical",
        posture="defensive", strategy_confidence=1.0,
        predicted_opponent_action="unknown",
        opponent_archetype="unknown", opponent_confidence=0.0,
        final_actions=["PASS"], primary_action="PASS",
    )


def _emergency_pass(time_result) -> TurnDecision:
    return TurnDecision(
        timing_directive="FORCE_PASS",
        time_remaining=time_result.get("time_remaining", 0.0) if isinstance(time_result, dict) else 0.0,
        hand_score=0.0, priority_profile="defensive",
        top_play="(time emergency)", strategy="time_critical",
        posture="defensive", strategy_confidence=1.0,
        predicted_opponent_action="unknown",
        opponent_archetype="unknown", opponent_confidence=0.0,
        final_actions=["PASS"], primary_action="PASS",
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

