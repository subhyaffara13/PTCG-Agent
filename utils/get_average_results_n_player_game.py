
def get_average_results_n_player_game(seq_game, policy, num_sample=10):
  result_array = get_list_results_n_player_game(seq_game, policy, num_sample)
  return sum([sum(i) / len(i) for i in zip(*result_array)]) / len(result_array)

