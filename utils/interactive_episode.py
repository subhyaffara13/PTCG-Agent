
def interactive_episode(
    env, num_players, num_actions, bot_names, learning_agent
):
  """Interactive Episode."""
  print("Starting interactive episode!")
  actions_str = ["R", "P", "S"]
  actions_seq = ["", ""]

  if FLAGS.interactive_mode == "human":
    pop_agent = HumanAgent(num_actions)
    pop_idx = -1
  else:
    test_pop_ids = [int(FLAGS.interactive_mode)]
    pop_agent, pop_idx = sample_bot_agent(bot_names, test_pop_ids, num_actions)
    print(f"Sampled bot {pop_idx} ({bot_names[pop_idx]})")

  agents = [pop_agent, learning_agent]

  time_step = env.reset()
  episode_rewards = np.zeros(num_players)
  turn_num = 0

  while not time_step.last():
    player_id = time_step.observations["current_player"]
    if env.is_turn_based:
      agent_output = agents[player_id].step(time_step, is_evaluation=True)
      action_list = [agent_output.action]
    else:
      agents_output = [
          agent.step(time_step, is_evaluation=True) for agent in agents
      ]
      action_list = [agent_output.action for agent_output in agents_output]
    if action_list[0] == -1:
      # Restart episode.
      print("Restarting episode.")
      interactive_episode(
          env, num_players, num_actions, bot_names, learning_agent
      )
      return
    action_list_str = [actions_str[int(x)] for x in action_list]
    actions_seq[0] += action_list_str[0]
    actions_seq[1] += action_list_str[1]
    predictions = last_predictions(learning_agent)
    indices = np.argsort(predictions)
    top_10_preds = pretty_top10_preds_str(predictions, indices, max_weight=0.75)
    time_step = env.step(action_list)
    episode_rewards += time_step.rewards
    print(
        f"Turn {turn_num}, Prev actions: {action_list_str}, "
        + f"Rewards: {time_step.rewards}, Returns: {episode_rewards} \n"
        + f"Action Seq [0]: {actions_seq[0]} \n"
        + f"Action Seq [1]: {actions_seq[1]}"
    )
    print(f"Top 10 predictions: \n{top_10_preds}")
    if FLAGS.interactive_mode != "human":
      # Prompt to continue.
      input("Press any key:")
    turn_num += 1

