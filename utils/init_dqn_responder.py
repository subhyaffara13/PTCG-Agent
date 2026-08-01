
def init_dqn_responder(env):
  """Initializes the Policy Gradient-based responder and agents."""
  state_representation_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  agent_class = rl_policy.DQNPolicy
  agent_kwargs = {
      "state_representation_size": state_representation_size,
      "num_actions": num_actions,
      "hidden_layers_sizes": [FLAGS.hidden_layer_size] * FLAGS.n_hidden_layers,
      "batch_size": FLAGS.batch_size,
      "learning_rate": FLAGS.dqn_learning_rate,
      "update_target_network_every": FLAGS.update_target_network_every,
      "learn_every": FLAGS.learn_every,
      "optimizer_str": FLAGS.optimizer_str
  }
  oracle = rl_oracle.RLOracle(
      env,
      agent_class,
      agent_kwargs,
      number_training_episodes=FLAGS.number_training_episodes,
      self_play_proportion=FLAGS.self_play_proportion,
      sigma=FLAGS.sigma)

  agents = [
      agent_class(  # pylint: disable=g-complex-comprehension
          env,
          player_id,
          **agent_kwargs)
      for player_id in range(FLAGS.n_players)
  ]
  for agent in agents:
    agent.freeze()
  return oracle, agents

