
def num_features(game) -> int:
  """Returns a number of features used for regression.

  Args:
    game: An OpenSpiel's `Game`.

  Returns:
    int: number columns in the feature matrix.
  """
  return game.information_state_tensor_size() + game.num_distinct_actions()


def num_features(game) -> int:
  """Returns a number of features used for regression.

  Args:
    game: An OpenSpiel's `Game`.

  Returns:
    int: number columns in the feature matrix.
  """
  return game.information_state_tensor_size() + game.num_distinct_actions()

