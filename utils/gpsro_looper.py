import time

def gpsro_looper(env, oracle, agents):
  """Initializes and executes the GPSRO training loop."""
  sample_from_marginals = True  # TODO(somidshafiei) set False for alpharank
  training_strategy_selector = (FLAGS.training_strategy_selector or
                                strategy_selectors.probabilistic)

  g_psro_solver = psro_v2.PSROSolver(
      env.game,
      oracle,
      initial_policies=agents,
      training_strategy_selector=training_strategy_selector,
      rectifier=FLAGS.rectifier,
      sims_per_entry=FLAGS.sims_per_entry,
      number_policies_selected=FLAGS.number_policies_selected,
      meta_strategy_method=FLAGS.meta_strategy_method,
      prd_iterations=50000,
      prd_gamma=1e-10,
      sample_from_marginals=sample_from_marginals,
      symmetric_game=FLAGS.symmetric_game)

  start_time = time.time()
  for gpsro_iteration in range(FLAGS.gpsro_iterations):
    if FLAGS.verbose:
      print("Iteration : {}".format(gpsro_iteration))
      print("Time so far: {}".format(time.time() - start_time))
    g_psro_solver.iteration()
    meta_game = g_psro_solver.get_meta_game()
    meta_probabilities = g_psro_solver.get_meta_strategies()
    policies = g_psro_solver.get_policies()

    if FLAGS.verbose:
      print("Meta game : {}".format(meta_game))
      print("Probabilities : {}".format(meta_probabilities))

    # The following lines only work for sequential games for the moment.
    if env.game.get_type().dynamics == pyspiel.GameType.Dynamics.SEQUENTIAL:
      aggregator = policy_aggregator.PolicyAggregator(env.game)
      aggr_policies = aggregator.aggregate(
          range(FLAGS.n_players), policies, meta_probabilities)

      exploitabilities, expl_per_player = exploitability.nash_conv(
          env.game, aggr_policies, return_only_nash_conv=False)

      _ = print_policy_analysis(policies, env.game, FLAGS.verbose)
      if FLAGS.verbose:
        print("Exploitabilities : {}".format(exploitabilities))
        print("Exploitabilities per player : {}".format(expl_per_player))

