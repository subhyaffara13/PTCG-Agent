
def get_list_results_n_player_simulataneous_game(game, policy, num_sample=10):
  return [
      get_results_n_player_simultaneous_game(game, policy)
      for _ in range(num_sample)
  ]

