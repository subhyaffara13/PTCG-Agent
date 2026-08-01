
def evaluate_in_selfplay(agent_x, agent_y, payoff_batch, steps_count):
  """Evalute in selfplay.

  Args:
    agent_x: First agent.
    agent_y: Second agent.
    payoff_batch: Payoff matrix.
    steps_count: Number of steps.
  """
  payoff_batch_size = payoff_batch.shape[0]

  regret_sum_x = np.zeros(shape=[payoff_batch_size, 1, FLAGS.num_actions])
  regret_sum_y = np.zeros(shape=[payoff_batch_size, 1, FLAGS.num_actions])
  strategy_x = agent_x.initial_policy()
  strategy_y = agent_y.initial_policy()

  regrets_x, regrets_y = compute_regrets(payoff_batch, strategy_x, strategy_y)
  regret_sum_x += regrets_x
  regret_sum_y += regrets_y
  for s in range(steps_count):
    values_y = -jnp.matmul(strategy_x, payoff_batch)
    values_x = jnp.transpose(
        jnp.matmul(payoff_batch, jnp.transpose(strategy_y, [0, 2, 1])),
        [0, 2, 1])

    values_x = jnp.transpose(values_x, [0, 2, 1])
    values_y = jnp.transpose(values_y, [0, 2, 1])
    strategy_x = agent_x.next_policy(values_x)
    strategy_y = agent_y.next_policy(values_y)

    regrets_x, regrets_y = compute_regrets(payoff_batch, strategy_x, strategy_y)
    regret_sum_x += regrets_x
    regret_sum_y += regrets_y
    print(
        jnp.mean(
            jnp.max(
                jnp.concatenate([regret_sum_x, regret_sum_y], axis=2),
                axis=[1, 2]) / (s + 1)))

