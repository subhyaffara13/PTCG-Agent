
def ficticious_play(seq_game, number_of_iterations, compute_metrics=False):
  xfp_solver = fictitious_play.XFPSolver(seq_game)
  tick_time = time.time()
  for _ in range(number_of_iterations):
    xfp_solver.iteration()
  timing = time.time() - tick_time
  # print('done')
  # average_policies = xfp_solver.average_policy_tables()
  tabular_policy = policy_module.TabularPolicy(seq_game)
  if compute_metrics:
    nash_conv = exploitability.nash_conv(seq_game, xfp_solver.average_policy())
    average_policy_values = expected_game_score.policy_value(
        seq_game.new_initial_state(), [tabular_policy])
    return timing, tabular_policy, nash_conv, average_policy_values
  return timing, tabular_policy

