
def boltzmannq(state, fitness, temperature=1.):
  """Selection-mutation dynamics modeling Q-learning with Boltzmann exploration.

  For more details, see equation (10) page 15 in
  https://jair.org/index.php/jair/article/view/10952

  Args:
    state: Probability distribution as an `np.array(shape=num_strategies)`.
    fitness: Fitness vector as an `np.array(shape=num_strategies)`.
    temperature: A scalar parameter determining the rate of exploration.

  Returns:
    Time derivative of the population state.
  """
  exploitation = (1. / temperature) * replicator(state, fitness)
  exploration = (np.log(state) - state.dot(np.log(state).transpose()))
  return exploitation - state * exploration

