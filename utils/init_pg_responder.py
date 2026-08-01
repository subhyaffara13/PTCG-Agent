
def init_pg_responder(env):
  """Initializes the Policy Gradient-based responder and agents."""
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  agent_class = rl_policy.PGPolicy

  agent_kwargs = {
      "info_state_size": info_state_size,
      "num_actions": num_actions,
      "loss_str": FLAGS.loss_str,
      "loss_class": False,
      "hidden_layers_sizes": [FLAGS.hidden_layer_size] * FLAGS.n_hidden_layers,
      "entropy_cost": FLAGS.entropy_cost,
      "critic_learning_rate": FLAGS.critic_learning_rate,
      "pi_learning_rate": FLAGS.pi_learning_rate,
      "num_critic_before_pi": FLAGS.num_q_before_pi,
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

