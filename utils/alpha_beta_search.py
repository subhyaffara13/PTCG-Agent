
def alpha_beta_search(game,
                      state=None,
                      value_function=None,
                      maximum_depth=30,
                      maximizing_player_id=None):
  """Solves deterministic, 2-players, perfect-information 0-sum game.

  For small games only! Please use keyword arguments for optional arguments.

  Arguments:
    game: The game to analyze, as returned by `load_game`.
    state: The state to run from, as returned by `game.new_initial_state()`.  If
      none is specified, then the initial state is assumed.
    value_function: An optional function mapping a Spiel `State` to a numerical
      value, to be used as the value of the maximizing player for a node when we
      reach `maximum_depth` and the node is not terminal.
    maximum_depth: The maximum depth to search over. When this depth is reached,
      an exception will be raised.
    maximizing_player_id: The id of the MAX player. The other player is assumed
      to be MIN. The default (None) will suppose the player at the root to be
      the MAX player.

  Returns:
    A tuple containing the value of the game for the maximizing player when
    both player play optimally, and the action that achieves this value.
  """
  game_info = game.get_type()

  if game.num_players() != 2:
    raise ValueError("Game must be a 2-player game")
  if game_info.chance_mode != pyspiel.GameType.ChanceMode.DETERMINISTIC:
    raise ValueError("The game must be a Deterministic one, not {}".format(
        game.chance_mode))
  if game_info.information != pyspiel.GameType.Information.PERFECT_INFORMATION:
    raise ValueError(
        "The game must be a perfect information one, not {}".format(
            game.information))
  if game_info.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
    raise ValueError("The game must be turn-based, not {}".format(
        game.dynamics))
  if game_info.utility != pyspiel.GameType.Utility.ZERO_SUM:
    raise ValueError("The game must be 0-sum, not {}".format(game.utility))

  if state is None:
    state = game.new_initial_state()
  if maximizing_player_id is None:
    maximizing_player_id = state.current_player()
  return _alpha_beta(
      state.clone(),
      maximum_depth,
      alpha=-float("inf"),
      beta=float("inf"),
      value_function=value_function,
      maximizing_player_id=maximizing_player_id)

