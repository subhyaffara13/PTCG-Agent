
def create_training_agents(
    num_players, num_actions, info_state_size, hidden_layers_sizes
):
  """Create the agents we want to use for learning."""
  if FLAGS.learner == "qlearning":
    # pylint: disable=g-complex-comprehension
    return [
        tabular_qlearner.QLearner(
            player_id=idx,
            num_actions=num_actions,
            # step_size=0.02,
            step_size=0.1,
            # epsilon_schedule=rl_tools.ConstantSchedule(0.5),
            epsilon_schedule=rl_tools.LinearSchedule(0.5, 0.2, 1000000),
            discount_factor=0.99) for idx in range(num_players)
    ]
  elif FLAGS.learner == "dqn":
    # pylint: disable=g-complex-comprehension
    return [
        dqn.DQN(
            player_id=idx,
            state_representation_size=info_state_size,
            num_actions=num_actions,
            discount_factor=0.99,
            epsilon_start=0.5,
            epsilon_end=0.1,
            hidden_layers_sizes=hidden_layers_sizes,
            replay_buffer_capacity=FLAGS.replay_buffer_capacity,
            batch_size=FLAGS.batch_size) for idx in range(num_players)
    ]
  else:
    raise RuntimeError("Unknown learner")

