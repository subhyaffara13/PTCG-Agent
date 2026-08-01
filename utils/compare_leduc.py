
def compare_leduc():
  game = pyspiel.load_game("leduc_poker")
  compare_cfr_with_jax_cfr(game)

