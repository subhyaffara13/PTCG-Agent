import time

def counterfactual_regret_minimization(seq_game,
                                       number_of_iterations,
                                       compute_metrics=False):
  # freq_iteration_printing = number_of_iterations // 10
  cfr_solver = cfr.CFRSolver(seq_game)
  tick_time = time.time()
  # print("CFRSolver initialized.")
  for _ in range(number_of_iterations):
    cfr_solver.evaluate_and_update_policy()
    # if i % freq_iteration_printing == 0:
    #   print(f"Iteration {i}")
  timing = time.time() - tick_time
  # print("Finish.")
  if compute_metrics:
    nash_conv = exploitability.nash_conv(seq_game, cfr_solver.average_policy())
    return timing, cfr_solver.average_policy(), nash_conv
  return timing, cfr_solver.average_policy()

