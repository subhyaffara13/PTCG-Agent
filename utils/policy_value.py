from typing import List, Union

def policy_value(state,
                 policies: Union[List[policy.Policy], policy.Policy],
                 probability_threshold: float = 0):
  """Returns the expected values for the state for players following `policies`.

  Computes the expected value of the`state` for each player, assuming player `i`
  follows the policy given in `policies[i]`.

  Args:
    state: A `pyspiel.State`.
    policies: A `list` of `policy.Policy` objects, one per player for sequential
      games, one policy for simulatenous games.
    probability_threshold: only sum over entries with prob greater than this
      (default: 0).

  Returns:
    A `numpy.array` containing the expected value for each player.
  """
  if state.is_terminal():
    return np.array(state.returns())
  else:
    return sum(prob * policy_value(policy.child(state, action), policies)
               for action, prob in _transitions(state, policies)
               if prob > probability_threshold)

