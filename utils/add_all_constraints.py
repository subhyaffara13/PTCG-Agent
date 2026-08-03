import itertools
from typing import Any, List

def add_all_constraints(
    game: coalitional_game.CoalitionalGame,
    x: cp.Variable,
    e: cp.Variable,
    constraints: List[Any]):
  # \sum x_i + e >= v(S), for all subsets S \subseteq N
  for c in itertools.product([0, 1], repeat=game.num_players()):
    coalition = np.asarray(c)
    val_coalition = game.coalition_value(coalition)
    constraints.append(x @ coalition + e >= val_coalition)

