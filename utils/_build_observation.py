
def _build_observation(state: pyspiel.State) -> dict[str, Any]:
    """Build a harness-style observation dict from a pyspiel connect_four state."""
    game = state.get_game()
    player_id = state.current_player()
    return {
        "observationString": state.observation_string(player_id),
        "playerId": player_id,
        "currentPlayer": player_id,
        "serializedGameAndState": pyspiel.serialize_game_and_state(game, state),
    }


def _build_observation(state: pyspiel.State) -> dict[str, Any]:
    """Build a harness-style observation dict from a pyspiel chess state."""
    game = state.get_game()
    player_id = state.current_player()
    return {
        "observationString": state.observation_string(player_id),
        "playerId": player_id,
        "currentPlayer": player_id,
        "serializedGameAndState": pyspiel.serialize_game_and_state(game, state),
    }

