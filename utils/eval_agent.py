
def eval_agent(env, agent, num_episodes):
  """Evaluates `agent` for `num_episodes`."""
  rewards = 0.0
  for _ in range(num_episodes):
    time_step = env.reset()
    episode_reward = 0
    while not time_step.last():
      agent_output = agent.step(time_step, is_evaluation=True)
      time_step = env.step([agent_output.action])
      episode_reward += time_step.rewards[0]
    rewards += episode_reward
  return rewards / num_episodes


def eval_agent(
    env,
    num_players,
    num_actions,
    bot_names,
    learning_agent,
    prediction_logger,
    num_training_episodes,
):
  """Evaluate the agent."""
  sum_episode_rewards = np.zeros(num_players)
  pop_expl = np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)
  for pop_idx in range(len(bot_names)):
    bot_id = pop_idx
    bot_name = bot_names[bot_id]
    bot = pyspiel.make_roshambo_bot(0, bot_name)
    pop_agent = BotAgent(num_actions, bot, name=bot_name)

    if hasattr(learning_agent, "restart"):
      learning_agent.restart()

    agents = [pop_agent, learning_agent]
    env.set_prediction_label(pop_idx)

    time_step = env.reset()
    episode_rewards = np.zeros(num_players)
    turn_num = 0
    prediction_logger.new_log(num_training_episodes)

    while not time_step.last():
      turn_num += 1
      player_id = time_step.observations["current_player"]
      if env.is_turn_based:
        agent_output = agents[player_id].step(time_step, is_evaluation=True)
        action_list = [agent_output.action]
      else:
        agents_output = [
            agent.step(time_step, is_evaluation=True) for agent in agents
        ]
        action_list = [agent_output.action for agent_output in agents_output]
      prediction_logger.log(
          num_training_episodes, pop_idx, last_predictions(learning_agent)
      )
      time_step = env.step(action_list)
      episode_rewards += time_step.rewards
    pop_expl[pop_idx] = episode_rewards[0]
    sum_episode_rewards += episode_rewards
    prediction_logger.end_log(num_training_episodes, pop_idx)
  prediction_logger.update_training_episodes(num_training_episodes)
  return sum_episode_rewards / len(bot_names), pop_expl

