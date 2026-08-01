
def get_expected_value(seq_game, policy, num_sample, player=0):
  results = get_list_results_n_player_game(
      seq_game, policy, num_sample=num_sample)
  expected_value = sum(x[player] for x in results) / num_sample
  # num_vehicle = len(results[0])
  # error_bar = abs(sum([x[1] for x in results]) - sum(
  # [x[2] for x in results])) / num_sample_trajectories
  # expected_value_policy = sum(sum(x[i] for x in results) for i in range(
  # 1, BRAESS_NUM_VEHICLES)) / ((BRAESS_NUM_VEHICLES-1)*num_sample_trajectories)
  return expected_value

