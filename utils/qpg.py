
def qpg(state, fitness):
  """Q-based policy gradient dynamics (QPG).

  For more details, see equation (12) on page 18 in
  https://arxiv.org/pdf/1810.09026.pdf

  Args:
    state: Probability distribution as an `np.array(shape=num_strategies)`.
    fitness: Fitness vector as an `np.array(shape=num_strategies)`.

  Returns:
    Time derivative of the population state.
  """
  regret = fitness - state.dot(fitness)
  return state * (state * regret - np.sum(state**2 * regret))

