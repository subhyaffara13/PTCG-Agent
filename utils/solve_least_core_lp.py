from typing import Tuple

def solve_least_core_lp(
    game: coalitional_game.CoalitionalGame,
    constraint_function: ConstraintsSamplingFuncType,
) -> Tuple[np.ndarray, float]:
  """Solve the LP described in Yan & Procaccia, equation (1).

  This LP enumerates all (exponentially many!) possible coalitions, with one
  constraint per coalition. Will not scale to games with too many players.

  Args:
    game: the game the LP solves.
    constraint_function: function that adds the constraints

  Returns:
    solution: an array with num_players entries,
    epsilon: the lowest epsilon.
  """
  # TODO(author5): handle errors gracefully. E.g. if solving the LP fails.

  num_players = game.num_players()
  val_gc = game.coalition_value(np.ones(game.num_players()))

  # min e
  # indices 0 - n-1 correspond to x_i, index n corresponds to e
  x = cp.Variable(num_players, nonneg=True)
  e = cp.Variable()  # note: epsilon can be negative when the core is non-empty!

  objective = cp.Minimize(e)
  constraints = []

  # \sum_{i in N} x_i  = v(N)
  constraints.append(x @ np.ones(num_players) == val_gc)

  # Add the constraints
  constraint_function(game, x, e, constraints)

  prob = cp.Problem(objective, constraints)
  _ = prob.solve(solver=cp.SCS, eps=1e-6)
  # The optimal value for x is stored in `x.value`.

  return x.value, e.value

