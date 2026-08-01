
def _get_preset_chance_action(
    env: core.Environment,
    os_state: pyspiel.State,
    outcomes: tuple[int, ...],
) -> int | None:
    preset_state = env.info.get("presetHandsState")
    if not preset_state:
        return None
    hand_idx = len(os_state.acpc_hand_histories())
    current_hand_index: int = preset_state["current_hand_index"]
    hands: list[tuple[int, ...]] = preset_state["hands"]
    next_index: list[int] = preset_state["next_index"]
    if hand_idx > current_hand_index:
        preset_state["current_hand_index"] = hand_idx
    if hand_idx >= len(hands):
        raise ValueError(f"Ran out of presetHands entries while attempting to start hand {hand_idx}.")
    hand_actions = hands[hand_idx]
    action_pos = next_index[hand_idx]
    if action_pos >= len(hand_actions):
        raise ValueError(f"presetHands[{hand_idx}] does not contain enough chance actions for the hand.")
    next_action = hand_actions[action_pos]
    if next_action not in outcomes:
        raise ValueError(
            f"presetHands[{hand_idx}] specified chance action {next_action} which is not available in the current chance outcomes."
        )
    next_index[hand_idx] = action_pos + 1
    return next_action

