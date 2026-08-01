
def confirm_chance_action_range(deck_size: int) -> None:
    """Confirm that OpenSpiel emits chance actions in [0, deck_size)."""
    try:
        import pyspiel  # type: ignore
    except ImportError:  # pragma: no cover - pyspiel unavailable in many dev envs.
        LOGGER.warning("pyspiel not installed; skipping chance action verification.")
        return

    game = pyspiel.load_game("repeated_poker")
    state = game.new_initial_state()
    if not state.is_chance_node():
        LOGGER.debug("Initial state not a chance node; advancing until chance.")
        while not state.is_terminal() and not state.is_chance_node():
            legal = state.legal_actions()
            if not legal:
                break
            state.apply_action(legal[0])

    if not state.is_chance_node():
        raise RuntimeError("Failed to reach a chance node while verifying deck range.")

    outcomes, _ = zip(*state.chance_outcomes())
    observed = set(outcomes)
    expected = set(range(deck_size))
    if observed != expected:
        raise ValueError(
            "Unexpected chance action range: "
            f"observed {min(observed)}-{max(observed)} covering {len(observed)} actions, "
            f"expected {deck_size} actions spanning 0-{deck_size - 1}."
        )
    LOGGER.info(
        "Verified OpenSpiel chance actions span 0-%d (%d entries).",
        deck_size - 1,
        deck_size,
    )

