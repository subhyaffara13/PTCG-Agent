
def neural_ficticious_self_play(seq_game,
                                num_epoch,
                                compute_metrics=False):
  env = rl_environment.Environment(seq_game)
  # Parameters from the game.
  num_players = env.num_players
  num_actions = env.action_spec()["num_actions"]
  info_state_size = env.observation_spec()["info_state"][0]

  # Parameters for the algorithm.
  hidden_layers_sizes = [int(l) for l in [128]]

  kwargs = {
      "replay_buffer_capacity": int(2e5),
      "reservoir_buffer_capacity": int(2e6),
      "min_buffer_size_to_learn": 1000,
      "anticipatory_param": 0.1,
      "batch_size": 128,
      "learn_every": 64,
      "rl_learning_rate": 0.01,
      "sl_learning_rate": 0.01,
      "optimizer_str": "sgd",
      "loss_str": "mse",
      "update_target_network_every": 19200,
      "discount_factor": 1.0,
      "epsilon_decay_duration": int(20e6),
      "epsilon_start": 0.06,
      "epsilon_end": 0.001,
  }

  # freq_epoch_printing = num_epoch // 10
  agents = [
      nfsp.NFSP(
          idx, info_state_size, num_actions, hidden_layers_sizes, **kwargs
      )
      for idx in range(num_players)
  ]
  joint_avg_policy = NFSPPolicies(env, agents, nfsp.MODE.average_policy)

  tick_time = time.time()
  for _ in range(num_epoch):
    # if ep % freq_epoch_printing == 0:
    #   print(f"Iteration {ep}")
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)
  timing = time.time() - tick_time
  # print("Finish.")
  if compute_metrics:
    tabular_policy = joint_avg_policy.TabularPolicy(seq_game)
    average_policy_values = expected_game_score.policy_value(
        seq_game.new_initial_state(), [tabular_policy])
    nash_conv = exploitability.nash_conv(env.game, joint_avg_policy)
    return timing, joint_avg_policy, average_policy_values, nash_conv
  return timing, joint_avg_policy

