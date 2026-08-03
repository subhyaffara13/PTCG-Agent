import time

def compare_cfr_with_jax_cfr(game):
  """Do the comparison."""

  start = time.time()
  jax_cfr = JaxCFR(game)
  print(time.time() - start)
  jax_cfr.multiple_steps(10000)
  print(time.time() - start)

  start = time.time()
  print(time.time() - start)
  cfr = CFRPlusSolver(game)
  for _ in range(1000):
    cfr.evaluate_and_update_policy()

  print(time.time() - start)

  jax_strat = jax_cfr.average_policy()
  jax_br1 = BestResponsePolicy(jax_cfr.game, 1, jax_strat)
  jax_br2 = BestResponsePolicy(jax_cfr.game, 0, jax_strat)

  cfr_strat = jax_cfr.average_policy()
  cfr_br1 = BestResponsePolicy(jax_cfr.game, 1, cfr_strat)
  cfr_br2 = BestResponsePolicy(jax_cfr.game, 0, cfr_strat)

  print("Jax P1: ", jax_br1.value(jax_cfr.game.new_initial_state()))
  print("CFR P1: ", cfr_br1.value(jax_cfr.game.new_initial_state()))
  print("Jax P2: ", jax_br2.value(jax_cfr.game.new_initial_state()))
  print("CFR P2: ", cfr_br2.value(jax_cfr.game.new_initial_state()))

