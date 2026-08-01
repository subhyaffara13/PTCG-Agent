
def compute_and_report_alpharank(payoff_tables,
                                 m=50,
                                 alpha=100,
                                 verbose=False,
                                 num_top_strats_to_print=8):
  """Computes and visualizes Alpha-Rank outputs.

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a numpy array, or a _PayoffTableInterface
      object.
    m: Finite population size.
    alpha: Fermi distribution temperature parameter.
    verbose: Set to True to print intermediate results.
    num_top_strats_to_print: Number of top strategies to print.

  Returns:
    pi: AlphaRank stationary distribution/rankings.
  """
  payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)
  rhos, rho_m, pi, _, _ = compute(payoff_tables, m=m, alpha=alpha)
  strat_labels = utils.get_strat_profile_labels(payoff_tables,
                                                payoffs_are_hpt_format)

  if verbose:
    print_results(payoff_tables, payoffs_are_hpt_format, pi=pi)

  utils.print_rankings_table(
      payoff_tables,
      pi,
      strat_labels,
      num_top_strats_to_print=num_top_strats_to_print)
  m_network_plotter = alpharank_visualizer.NetworkPlot(
      payoff_tables, rhos, rho_m, pi, strat_labels, num_top_profiles=8)
  m_network_plotter.compute_and_draw_network()
  return pi

