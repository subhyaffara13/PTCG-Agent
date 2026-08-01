
def game_payoffs_array(game):
  """Returns a `numpy.ndarray` of utilities for a game.

  NOTE: if the game is not a MatrixGame or a TensorGame then this may be costly.

  Args:
    game: A game.

  Returns:
    `numpy.ndarray` of dimension `num_players` + 1.
    First dimension is the player, followed by the actions of all players, e.g.
    a 3x3 game (2 players) has dimension [2,3,3].
  """
  if isinstance(game, pyspiel.MatrixGame):
    return np.stack([game.row_utilities(), game.col_utilities()])

  if not isinstance(game, pyspiel.TensorGame):
    game = pyspiel.extensive_to_tensor_game(game)
  return np.stack(
      [game.player_utilities(player) for player in range(game.num_players())])

