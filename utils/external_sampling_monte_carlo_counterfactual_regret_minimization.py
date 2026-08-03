import time

def external_sampling_monte_carlo_counterfactual_regret_minimization(
    seq_game, number_of_iterations, compute_metrics=False):
  cfr_solver = external_mccfr.ExternalSamplingSolver(
      seq_game, external_mccfr.AverageType.SIMPLE)
  tick_time = time.time()
  # print("CFRSolver initialized.")
  for _ in range(number_of_iterations):
    cfr_solver.iteration()
  timing = time.time() - tick_time
  # print("Finish.")
  if compute_metrics:
    nash_conv = exploitability.nash_conv(seq_game, cfr_solver.average_policy())
    return timing, cfr_solver.average_policy(), nash_conv
  return timing, cfr_solver.average_policy()

