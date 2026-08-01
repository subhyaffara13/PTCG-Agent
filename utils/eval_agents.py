
def eval_agents(env, agents, num_episodes):
  """Evaluate the agents, returning a numpy array of average returns."""
  rewards = np.array([0] * env.num_players, dtype=np.float64)
  for _ in range(num_episodes):
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step, is_evaluation=True)
      time_step = env.step([agent_output.action])
    for i in range(env.num_players):
      rewards[i] += time_step.rewards[i]
  rewards /= num_episodes
  return rewards


def eval_agents(env, agents, num_players, num_episodes):
  """Evaluate the agent."""
  sum_episode_rewards = np.zeros(num_players)
  for ep in range(num_episodes):
    for agent in agents:
      # Bots need to be restarted at the start of the episode.
      if hasattr(agent, "restart"):
        agent.restart()
    time_step = env.reset()
    episode_rewards = np.zeros(num_players)
    while not time_step.last():
      agents_output = [
          agent.step(time_step, is_evaluation=True) for agent in agents
      ]
      action_list = [agent_output.action for agent_output in agents_output]
      time_step = env.step(action_list)
      episode_rewards += time_step.rewards
    sum_episode_rewards += episode_rewards
    print(f"Finished episode {ep}, "
          + f"avg returns: {sum_episode_rewards / num_episodes}")

  return sum_episode_rewards / num_episodes

