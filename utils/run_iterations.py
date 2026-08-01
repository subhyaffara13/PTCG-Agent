
def run_iterations(game, solver, start_iteration=0):
  """Run iterations of MCCFR."""
  for i in range(int(FLAGS.iterations / 2)):
    solver.run_iteration()
    policy = solver.average_policy()
    exploitability = pyspiel.exploitability(game, policy)

    # We also compute NashConv to highlight an important API feature:
    # when using Monte Carlo sampling, the policy
    # may not have a table entry for every info state.
    # Therefore, when calling nash_conv, ensure the third argument,
    # "use_state_get_policy" is set to True
    # See https://github.com/deepmind/open_spiel/issues/500
    nash_conv = pyspiel.nash_conv(game, policy, True)

    print("Iteration {} nashconv: {:.6f} exploitability: {:.6f}".format(
        start_iteration + i, nash_conv, exploitability))

