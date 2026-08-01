
def make_iterated_matrix_game(
    game: str, iterations=5, batch_size=8
) -> rl_environment.Environment:
  matrix_game = pyspiel.load_matrix_game(game)
  config = {'num_repetitions': iterations, 'batch_size': batch_size}
  game = pyspiel.create_repeated_game(matrix_game, config)
  env = rl_environment.Environment(game)
  return env

