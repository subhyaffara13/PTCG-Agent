
def evaluate_against_best_response(agent, payoff_batch, steps_count):
  """Evaluation against best response agent.

  Args:
    agent: Agent model.
    payoff_batch: Payoff matrix.
    steps_count: Number of steps.
  """
  current_policy = agent.initial_policy()
  values = jax.vmap(compute_values_against_best_response)(current_policy,
                                                          payoff_batch)
  for step in range(steps_count):
    current_policy = agent.next_policy(values)
    values = jax.vmap(compute_values_against_best_response)(current_policy,
                                                            payoff_batch)
    values = jnp.transpose(values, [0, 1, 2])
    value = jnp.matmul(current_policy, values)

    for i in range(value.shape[0]):
      print(step, np.mean(np.asarray(value[i])))

