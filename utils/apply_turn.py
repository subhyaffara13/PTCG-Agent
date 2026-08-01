
def apply_turn(state: SessionState, turn: Turn) -> SignalDelta:
    """
    Detect signals on this turn, mutate state, return the delta.

    O(1) per turn (no full-history rescan). Only inspects last_*, recent tool history
    (which is bounded at TOOL_CALL_HISTORY_MAX), and the new turn payload.
    """
    delta = SignalDelta()

    if _detect_misalignment(state.last_user_content, turn.user_content):
        delta.misalignment = 1
    if _detect_stagnation(state.last_assistant_content, turn.assistant_content):
        delta.stagnation = 1
    if _detect_disengagement(turn.user_content):
        delta.disengagement = 1
    if _detect_satisfaction(turn.user_content):
        # Gate: only award satisfaction credit once per session, and only
        # after MIN_TURNS_FOR_CLEAN_CREDIT turns of context. Early "thanks"
        # on turn 1-2 is noise, not a validated quality signal.
        current_turn_index = state.turn_count + 1
        if (
            not state.clean_credit_awarded
            and current_turn_index >= MIN_TURNS_FOR_CLEAN_CREDIT
        ):
            delta.satisfaction = 1
            state.clean_credit_awarded = True
    if _detect_failure(turn.tool_results):
        delta.failure = 1
    if _detect_loop(state.tool_call_history, turn.tool_calls):
        delta.loop = 1
    if _detect_exhaustion(turn.response_status, turn.tool_results):
        delta.exhaustion = 1

    state.misalignment_count += delta.misalignment
    state.stagnation_count += delta.stagnation
    state.disengagement_count += delta.disengagement
    state.satisfaction_count += delta.satisfaction
    state.failure_count += delta.failure
    state.loop_count += delta.loop
    state.exhaustion_count += delta.exhaustion

    if turn.user_content:
        state.last_user_content = turn.user_content
    if turn.assistant_content:
        state.last_assistant_content = turn.assistant_content

    for call in turn.tool_calls:
        state.tool_call_history.append(_signature(call))
    if len(state.tool_call_history) > TOOL_CALL_HISTORY_MAX:
        state.tool_call_history = state.tool_call_history[-TOOL_CALL_HISTORY_MAX:]

    if turn.response_status is not None:
        state.terminal_status = turn.response_status

    state.turn_count += 1
    state.last_processed_turn = state.turn_count

    return delta

