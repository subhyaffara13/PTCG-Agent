
def get_alg_config():
  """Get configuration for botched trades experiment."""
  alg_config = configdict.ConfigDict()

  alg_config.init = configdict.ConfigDict()
  alg_config.init.lr_primal = 1e-2
  alg_config.init.lr_dual = 1e-2

  alg_config.solve = configdict.ConfigDict()
  alg_config.solve.batch_size = 2**3
  alg_config.solve.mu_init = 1000
  alg_config.solve.gamma = 1e-8
  alg_config.solve.n_iter = 110_000
  alg_config.solve.seed = 0
  alg_config.solve.save_every = 10_000

  alg_config.eval = configdict.ConfigDict()
  alg_config.eval.evaluation_iterations = 2**3

  return alg_config

