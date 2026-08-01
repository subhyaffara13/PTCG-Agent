
def replicator(state, fitness):
  """Continuous-time replicator dynamics.

  This is the standard form of the continuous-time replicator dynamics also
  known as selection dynamics.

  For more details, see equation (5) page 9 in
  https://jair.org/index.php/jair/article/view/10952

  Args:
    state: Probability distribution as an `np.array(shape=num_strategies)`.
    fitness: Fitness vector as an `np.array(shape=num_strategies)`.

  Returns:
    Time derivative of the population state.
  """
  avg_fitness = state.dot(fitness)
  return state * (fitness - avg_fitness)

