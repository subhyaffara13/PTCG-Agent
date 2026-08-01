
def get_list_results_n_player_game(seq_game, policy, num_sample=10):
  return [
      get_results_n_player_sequential_game(seq_game, policy)
      for _ in range(num_sample)
  ]

