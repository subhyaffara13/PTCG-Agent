import copy

def run_experiment(num_players, env, payoffs, centralized):
  """Run the experiments."""
  num_states = FLAGS.num_states
  num_messages = FLAGS.num_messages
  num_actions = env.action_spec()["num_actions"]

  # Results to store
  num_runs = FLAGS.num_runs
  training_episodes = FLAGS.num_episodes
  log_interval = FLAGS.log_interval
  rewards = np.zeros((num_runs, training_episodes // log_interval))
  opts = np.zeros((num_runs, training_episodes // log_interval))
  converge_point = np.zeros((num_states, num_states))
  percent_opt = 0

  # Repeat the experiment num_runs times
  for i in range(num_runs):
    eps_schedule = rl_tools.LinearSchedule(
        FLAGS.eps_init, FLAGS.eps_final, FLAGS.eps_decay_steps *
        2)  # *2 since there are 2 agent steps per episode

    agents = [
        # pylint: disable=g-complex-comprehension
        tabular_qlearner.QLearner(
            player_id=idx,
            num_actions=num_actions,
            step_size=FLAGS.step_size,
            epsilon_schedule=eps_schedule,
            centralized=centralized) for idx in range(num_players)
    ]

    # 1. Train the agents
    for cur_episode in range(training_episodes):
      time_step = env.reset()
      # Find cur_state for logging. See lewis_signaling.cc for info_state
      # details.
      cur_state = time_step.observations["info_state"][0][3:].index(1)
      while not time_step.last():
        player_id = time_step.observations["current_player"]
        agent_output = agents[player_id].step(time_step)
        time_step = env.step([agent_output.action])

      # Episode is over, step all agents with final info state.
      for agent in agents:
        agent.step(time_step)

      # Store rewards
      reward = time_step.rewards[0]
      max_reward = payoffs[cur_state].max()
      cur_idx = (i, cur_episode // log_interval)
      rewards[cur_idx] += reward / log_interval
      opts[cur_idx] += np.isclose(reward, max_reward) / log_interval

    base_info_state0 = [1.0, 0.0, 0.0] + [0.0] * num_states
    base_info_state1 = [0.0, 1.0, 0.0] + [0.0] * num_states
    if centralized:
      base_info_state0 = [base_info_state0, base_info_state0.copy()]
      base_info_state1 = [base_info_state1, base_info_state1.copy()]

    for s in range(num_states):
      info_state0 = copy.deepcopy(base_info_state0)
      if centralized:
        info_state0[0][3 + s] = 1.0
      else:
        info_state0[3 + s] = 1.0
      # pylint: disable=protected-access
      m, _ = agents[0]._epsilon_greedy(
          str(info_state0), np.arange(num_messages), 0)
      info_state1 = copy.deepcopy(base_info_state1)
      if centralized:
        info_state1[0][3 + s] = 1.0
        info_state1[1][3 + m] = 1.0
      else:
        info_state1[3 + m] = 1.0
      a, _ = agents[1]._epsilon_greedy(
          str(info_state1), np.arange(num_states), 0)
      converge_point[s, a] += 1
      best_act = payoffs[s].argmax()
      percent_opt += int(a == best_act) / num_runs / num_states
  return rewards, opts, converge_point, percent_opt


def run_experiment(
    output_dir, num_blocks, config, use_random_agents, debug, parallel, num_processes, shuffle_player_ids
):
    """
    Runs a tournament by generating all game tasks and processing them,
    potentially in parallel.
    """
    if debug:
        logger.warning("Debug mode is enabled. Forcing sequential execution.")

    base_game_config = config["game_config"]
    players_data = base_game_config["agents"]
    total_games = num_blocks * len(players_data)

    if parallel:
        logger.info(f"Running games in parallel with up to {num_processes} processes.")

    game_tasks = generate_game_tasks(output_dir, num_blocks, config, use_random_agents, debug, shuffle_player_ids)

    with tqdm(total=total_games, desc="Processing Games") as pbar:
        if parallel:
            with multiprocessing.Pool(processes=num_processes) as pool:
                for _ in pool.imap_unordered(game_runner_wrapper, game_tasks):
                    pbar.update(1)
        else:
            for task_args in game_tasks:
                game_runner_wrapper(task_args)
                pbar.update(1)

    logger.info("All game tasks have been processed.")

