
def _run_actions(state, game, actions, active_idx, game_player):
    """
    Execute the active agent's action list for the turn.

    Well-formed but illegal actions (unaffordable, occupied tile, out of
    range, at the per-player unit cap, unknown action/unit type) are skipped
    as no-ops and the turn continues. This suits the multi-action-per-turn
    API: one rejected action in a list shouldn't forfeit the whole episode,
    and ``get_legal_actions`` already lets agents avoid illegal moves. Only a
    malformed action (not a dict) is treated as a broken agent and forfeits.

    Always returns the list of actions the engine actually applied (up to
    and including the offending entry's predecessors on forfeit). The
    forfeit flag is signalled out-of-band via ``state[active_idx].status``,
    which ``_mark_agent_loss`` sets to ``"DONE"`` before returning -- so
    the caller can still overwrite ``agent.action`` with the partial
    executed list and surface this turn's ``action_log`` slice instead of
    leaving the prior turn's observation stale.
    """
    executed = []
    for action in actions:
        if not isinstance(action, dict):
            _mark_agent_loss(state, active_idx)
            return executed

        if action.get("type", "") == "end_turn":
            executed.append(action)
            break

        # Illegal-but-well-formed action: skip it (no-op) and keep going.
        if not _execute_action(game, action, game_player):
            continue

        executed.append(action)

        if game.game_over:
            break

    return executed

