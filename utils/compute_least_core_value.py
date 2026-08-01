
def compute_least_core_value(
    cvc: coalitional_game.CoalitionalGame, alg_config
) -> LeastCoreValue:
  """Computes the least core value of a game."""
  opt_primal = optax.adam(learning_rate=alg_config.init.lr_primal)
  opt_dual = optax.adam(learning_rate=alg_config.init.lr_dual)
  evaluation_iterations = alg_config.eval.evaluation_iterations
  evaluate_every = 2 * alg_config.solve.n_iter  # do not evaluate
  cl = CoreLagrangian(cvc, opt_primal, opt_dual)
  payoffs, epsilons, _, duration = cl.solve(
      evaluation_iterations=evaluation_iterations,
      evaluate_every=evaluate_every,
      **alg_config.solve,
  )
  lcvs = np.full(payoffs.shape[0], np.inf)
  payoff = payoffs[-1]
  lcv = np.inf
  for i in range(payoffs.shape[0]):
    payoff = payoffs[i]
    epsilon = epsilons[i]
    max_violation = payoff_evaluation(
        cvc, payoff, epsilon, evaluation_iterations)
    lcv = epsilon + max_violation
    lcvs[i] = lcv
  meta = dict(payoffs=payoffs, epsilons=epsilons, lcvs=lcvs)
  return LeastCoreValue(payoff, lcv, duration, meta)

