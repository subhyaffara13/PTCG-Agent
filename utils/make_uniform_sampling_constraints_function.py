from typing import Any, List

def make_uniform_sampling_constraints_function(
    num: int,
) -> ConstraintsSamplingFuncType:
  """Simple uniform constraint sampler (with replacement)."""

  def func(game: coalitional_game.CoalitionalGame,
           x: cp.Variable, e: cp.Variable, constraints: List[Any]):
    for _ in range(num):
      coalition = np.random.randint(2, size=game.num_players())
      val_coalition = game.coalition_value(coalition)
      constraints.append(x @ coalition + e >= val_coalition)
  return func

