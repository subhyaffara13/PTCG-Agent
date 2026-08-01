
def _q_learning_dynamics(composition, payoff, temperature):
  r"""An equivalent implementation of `dynamics.boltzmannq`."""
  return 1 / temperature * dynamics.replicator(composition, payoff) + (
      composition * _sum_j_x_j_ln_x_j_over_x_i(composition))

