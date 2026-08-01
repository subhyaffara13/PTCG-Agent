
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


def _merge(arr, temp, left, mid, right):
    """
    Merges two sorted arrays and calculates the inversion count.

    Helper function for calculating inversions. This method is
    for internal use only.
    """
    i = k = left
    j = mid
    inv_count = 0
    while i < mid and j <= right:
        if arr[i] < arr[j]:
            temp[k] = arr[i]
            k += 1
            i += 1
        else:
            temp[k] = arr[j]
            k += 1
            j += 1
            inv_count += (mid -i)
    while i < mid:
        temp[k] = arr[i]
        k += 1
        i += 1
    if j <= right:
        k += right - j + 1
        j += right - j + 1
        arr[left:k + 1] = temp[left:k + 1]
    else:
        arr[left:right + 1] = temp[left:right + 1]
    return inv_count

