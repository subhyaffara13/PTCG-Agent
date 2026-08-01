
def get_exact_value(
    pi: policy_std.Policy, mu: distribution_std.Distribution, game
):
  """Computes the exact value of playing `pi` against distribution `mu`.

  Args:
    pi: A policy object whose value is evaluated against `mu`.
    mu: A distribution object against which `pi` is evaluated.
    game: A pyspiel.Game object, the evaluation game.

  Returns:
    Exact value of `pi` in `game` against `mu`.
  """
  root_state = game.new_initial_states()[0]
  return policy_value.PolicyValue(game, mu, pi).value(root_state)

