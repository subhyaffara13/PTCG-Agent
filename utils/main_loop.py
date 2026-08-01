
def main_loop(unused_arg):
  """Trains a Policy Gradient agent in the catch environment."""
  env = catch.Environment()
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  train_episodes = FLAGS.num_episodes

  agent = policy_gradient.PolicyGradient(
      player_id=0,
      info_state_size=info_state_size,
      num_actions=num_actions,
      loss_str=FLAGS.algorithm,
      hidden_layers_sizes=[128, 128],
      lambda_=1.0,
      entropy_cost=0.01,
      critic_learning_rate=0.1,
      pi_learning_rate=0.1,
      num_critic_before_pi=3)

  # Train agent
  for ep in range(train_episodes):
    time_step = env.reset()
    while not time_step.last():
      agent_output = agent.step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)
    # Episode is over, step agent with final info state.
    agent.step(time_step)

    if ep and ep % FLAGS.eval_every == 0:
      logging.info("-" * 80)
      logging.info("Episode %s", ep)
      logging.info("Loss: %s", agent.loss)
      avg_return = _eval_agent(env, agent, 100)
      logging.info("Avg return: %s", avg_return)


def main_loop(unused_arg):
  """Trains a Policy Gradient agent in the catch environment."""
  env = catch.Environment()
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  train_episodes = FLAGS.num_episodes

  agent = policy_gradient.PolicyGradient(
      player_id=0,
      info_state_size=info_state_size,
      num_actions=num_actions,
      loss_str=FLAGS.algorithm,
      hidden_layers_sizes=[128, 128],
      batch_size=128,
      entropy_cost=0.01,
      critic_learning_rate=0.1,
      pi_learning_rate=0.1,
      num_critic_before_pi=3)

  # Train agent
  for ep in range(train_episodes):
    time_step = env.reset()
    while not time_step.last():
      agent_output = agent.step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)
    # Episode is over, step agent with final info state.
    agent.step(time_step)

    if ep and ep % FLAGS.eval_every == 0:
      logging.info("-" * 80)
      logging.info("Episode %s", ep)
      logging.info("Loss: %s", agent.loss)
      avg_return = _eval_agent(env, agent, 100)
      logging.info("Avg return: %s", avg_return)


def main_loop(unused_arg):
  """Trains a DQN agent in the catch environment."""
  env = catch.Environment()
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  train_episodes = FLAGS.num_episodes

  agent = dqn.DQN(
      player_id=0,
      state_representation_size=info_state_size,
      num_actions=num_actions,
      learning_rate=0.1,
      replay_buffer_capacity=10000,
      hidden_layers_sizes=[32, 32],
      epsilon_decay_duration=2000,  # 10% total data
      update_target_network_every=250,
  )

  # Train agent
  for ep in range(train_episodes):
    time_step = env.reset()
    while not time_step.last():
      agent_output = agent.step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)
    # Episode is over, step agent with final info state.
    agent.step(time_step)

    if ep and ep % FLAGS.eval_every == 0:
      logging.info("-" * 80)
      logging.info("Episode %s", ep)
      logging.info("Loss: %s", agent.loss)
      avg_return = _eval_agent(env, agent, 100)
      logging.info("Avg return: %s", avg_return)


def main_loop(unused_arg):
  """RL main loop example."""
  logging.info("Registered games: %s", rl_environment.registered_games())
  logging.info("Creating game %s", FLAGS.game)

  env_configs = {"players": FLAGS.num_players} if FLAGS.num_players else {}
  env = rl_environment.Environment(FLAGS.game, **env_configs)
  num_actions = env.action_spec()["num_actions"]

  agents = [
      random_agent.RandomAgent(player_id=i, num_actions=num_actions)
      for i in range(FLAGS.num_players)
  ]

  logging.info("Env specs: %s", env.observation_spec())
  logging.info("Action specs: %s", env.action_spec())

  for cur_episode in range(FLAGS.num_episodes):
    logging.info("Starting episode %s", cur_episode)
    time_step = env.reset()
    while not time_step.last():
      pid = time_step.observations["current_player"]

      if env.is_turn_based:
        agent_output = agents[pid].step(time_step)
        action_list = [agent_output.action]
      else:
        agents_output = [agent.step(time_step) for agent in agents]
        action_list = [agent_output.action for agent_output in agents_output]

      print_iteration(time_step, pid, action_list)
      time_step = env.step(action_list)

    # Episode is over, step all agents with final state.
    for agent in agents:
      agent.step(time_step)

    # Print final state of end game.
    for pid in range(env.num_players):
      print_iteration(time_step, pid)


def main_loop(unused_arg):
  """Trains a tabular qlearner agent in the cliff walking environment."""
  env = cliff_walking.Environment(width=5, height=3)
  num_actions = env.action_spec()["num_actions"]

  train_episodes = FLAGS.num_episodes
  eval_interval = 50

  agent = tabular_qlearner.QLearner(
      player_id=0, step_size=0.05, num_actions=num_actions)

  # Train the agent
  for ep in range(train_episodes):
    time_step = env.reset()
    while not time_step.last():
      agent_output = agent.step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)
    # Episode is over, step agent with final info state.
    agent.step(time_step)

    if ep and ep % eval_interval == 0:
      logging.info("-" * 80)
      logging.info("Episode %s", ep)
      logging.info("Last loss: %s", agent.loss)
      avg_return = eval_agent(env, agent, 100)
      logging.info("Avg return: %s", avg_return)

