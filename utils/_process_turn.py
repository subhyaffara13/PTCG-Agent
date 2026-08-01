
def _process_turn(state, env, game, active_idx, key):
    """Process actions, end turn, and check win/draw conditions."""
    agent = state[active_idx]
    actions = agent.action if agent.action else []

    if not isinstance(actions, list):
        actions = [actions]

    game_player = active_idx + 1  # GameState uses 1-indexed players

    # Snapshot the engine's action_history length so we can slice out the
    # entries appended during this turn (agent actions + end_turn) and
    # surface them in the replay.
    log_start = len(game.action_history)

    executed = _run_actions(state, game, actions, active_idx, game_player)

    # Replace the agent's submitted action list with the filtered version so
    # the replay records only the actions the engine actually applied --
    # otherwise rejected attacks/seizes/moves show up in the replay's
    # action[] and the visualizer draws highlights for actions that
    # never happened.
    agent.action = executed

    # Forfeit short-circuit: ``_run_actions`` already marked both agents
    # DONE via ``_mark_agent_loss``. Still surface this turn's
    # action_log slice (which captures any actions executed before the
    # malformed entry, plus is empty when the malformed action came first)
    # so the replay's final-step observation isn't a stale carry-over
    # from the prior turn.
    if state[active_idx].status == "DONE":
        _update_observations(state, game, _slice_action_log(game, log_start))
        _games.pop(key, None)
        return

    # End the turn (income, healing, status effects, etc.)
    if not game.game_over:
        game.end_turn()

    action_log = _slice_action_log(game, log_start)

    # Check win condition
    if game.game_over:
        if game.winner is None:
            # Draw (e.g., game's own max_turns cap)
            for i in range(2):
                state[i].reward = 0
                state[i].status = "DONE"
        else:
            winner_idx = game.winner - 1
            state[winner_idx].reward = 1
            state[winner_idx].status = "DONE"
            state[1 - winner_idx].reward = -1
            state[1 - winner_idx].status = "DONE"
        _update_observations(state, game, action_log)
        _games.pop(key, None)
        return

    # Check draw (max turns)
    if game.turn_number >= env.configuration.episodeSteps:
        for i in range(2):
            state[i].reward = 0
            state[i].status = "DONE"
        _update_observations(state, game, action_log)
        _games.pop(key, None)
        return

    # Normal continuation: update observations and swap active player
    _update_observations(state, game, action_log)
    state[active_idx].status = "INACTIVE"
    state[1 - active_idx].status = "ACTIVE"

