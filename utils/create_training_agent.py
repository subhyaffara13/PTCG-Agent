
def create_training_agent(
    agent_type,
    num_actions,
    info_state_size,
    hidden_layers_sizes,
    max_abs_reward,
    rng_seed,
    player_id,
):
  """Create training agent."""
  if agent_type == "dqn":
    return dqn.DQN(
        player_id=player_id,
        state_representation_size=info_state_size,
        num_actions=num_actions,
        discount_factor=0.99,
        epsilon_start=1.0,
        epsilon_end=0.1,
        hidden_layers_sizes=hidden_layers_sizes,
        learning_rate=FLAGS.learning_rate,
        replay_buffer_capacity=FLAGS.replay_buffer_capacity,
        batch_size=FLAGS.batch_size,
    )
  elif agent_type == "bdqn":
    return boltzmann_dqn.BoltzmannDQN(
        player_id=player_id,
        state_representation_size=info_state_size,
        num_actions=num_actions,
        discount_factor=0.99,
        epsilon_start=1.0,
        epsilon_end=0.1,
        hidden_layers_sizes=hidden_layers_sizes,
        learning_rate=FLAGS.learning_rate,
        replay_buffer_capacity=FLAGS.replay_buffer_capacity,
        batch_size=FLAGS.batch_size,
        eta=FLAGS.eta,
        seed=FLAGS.seed,
    )
  elif agent_type == "qlearning":
    return tabular_qlearner.QLearner(
        player_id=player_id,
        num_actions=num_actions,
        step_size=FLAGS.learning_rate,
        epsilon_schedule=rl_tools.LinearSchedule(0.5, 0.2, 1000000),
        discount_factor=0.99,
    )
  elif agent_type == "a2c":
    return policy_gradient.PolicyGradient(
        player_id,
        info_state_size,
        num_actions,
        loss_str="a2c",
        critic_learning_rate=FLAGS.critic_learning_rate,
        pi_learning_rate=FLAGS.pi_learning_rate,
        entropy_cost=FLAGS.entropy_cost,
        num_critic_before_pi=FLAGS.num_critic_before_pi,
        lambda_=FLAGS.lambda_,
        additional_discount_factor=0.99,
        hidden_layers_sizes=hidden_layers_sizes,
    )
  elif agent_type == "impala":
    return impala.IMPALA(  # pylint: disable=g-complex-comprehension
        player_id=player_id,
        state_representation_size=info_state_size,
        num_actions=num_actions,
        num_players=2,
        unroll_len=FLAGS.unroll_length,
        net_factory=impala.BasicRNN,
        rng_key=jax.random.PRNGKey(rng_seed),
        max_abs_reward=max_abs_reward,
        learning_rate=FLAGS.pi_learning_rate,
        entropy=FLAGS.entropy_cost,
        hidden_layers_sizes=hidden_layers_sizes,
        num_predictions=pyspiel.ROSHAMBO_NUM_BOTS + 1,
        prediction_weight=FLAGS.prediction_weight,
        batch_size=FLAGS.batch_size,
    )
  elif agent_type == "rm":
    return RegretMatchingAgent(
        player_id=player_id, num_actions=num_actions, epsilon=FLAGS.rm_epsilon
    )
  elif agent_type == "rock":
    return ConstantActionAgent(player_id, num_actions, 0)
  elif agent_type == "paper":
    return ConstantActionAgent(player_id, num_actions, 1)
  elif agent_type == "scissors":
    return ConstantActionAgent(player_id, num_actions, 2)
  elif agent_type == "uniform":
    return random_agent.RandomAgent(player_id, num_actions)
  else:
    assert False

