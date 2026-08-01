
def _drain_chance_actions(
    state: pyspiel.State,
    preset_hands: list[list[int]],
    next_index: list[int],
) -> None:
    """Advance through chance nodes, consuming the next preset card each time.

    Mirrors ``_get_preset_chance_action`` in ``open_spiel_env.py``.
    """
    while not state.is_terminal() and state.is_chance_node():
        hand_idx = len(state.acpc_hand_histories())
        if hand_idx >= len(preset_hands):
            raise ValueError(f"Ran out of preset hands at hand_idx={hand_idx}")
        pos = next_index[hand_idx]
        card = preset_hands[hand_idx][pos]
        next_index[hand_idx] = pos + 1
        state.apply_action(card)

