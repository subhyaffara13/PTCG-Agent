
def sweep_pi_vs_epsilon(payoff_tables,
                        strat_labels=None,
                        warm_start_epsilon=None,
                        visualize=False,
                        return_epsilon=False,
                        min_iters=10,
                        max_iters=100,
                        min_epsilon=1e-14,
                        num_strats_to_label=10,
                        legend_sort_clusters=False):
  """Computes infinite-alpha distribution for a range of perturbations.

  The range of response graph perturbations is defined in epsilon_list.

  Note that min_iters and max_iters is necessary as it may sometimes appear the
  stationary distribution has converged for a game in the first few iterations,
  where in reality a sufficiently smaller epsilon is needed for the distribution
  to first diverge, then reconverge. This behavior is dependent on both the
  payoff structure and bounds, so the parameters min_iters and max_iters can be
  used to fine-tune this.

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity.
      Each payoff_table may be either a numpy array, or a
      _PayoffTableInterface object.
    strat_labels: Human-readable strategy labels. See get_strat_profile_labels()
      in utils.py for formatting details.
    warm_start_epsilon: Initial value of epsilon to use.
    visualize: Plot the sweep results.
    return_epsilon: Whether to return the final epsilon used.
    min_iters: the minimum number of sweep iterations.
    max_iters: the maximum number of sweep iterations.
    min_epsilon: the minimum value of epsilon to be tested, at which point the
      sweep terminates (if not converged already).
    num_strats_to_label: Number of strats to label in legend
    legend_sort_clusters: If true, strategies in the same cluster are sorted in
      the legend according to orderings for earlier alpha values. Primarily for
      visualization purposes! Rankings for lower alpha values should be
      interpreted carefully.

  Returns:
   pi: AlphaRank stationary distribution.
   epsilon: The AlphaRank transition matrix noise level resulting from sweep.
  """
  payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)
  num_populations = len(payoff_tables)
  num_strats_per_population = utils.get_num_strats_per_population(
      payoff_tables, payoffs_are_hpt_format)

  if num_populations == 1:
    num_profiles = num_strats_per_population[0]
  else:
    num_profiles = utils.get_num_profiles(num_strats_per_population)

  if not (
      strat_labels is None
      or isinstance(strat_labels, dict)
      or (len(strat_labels) == num_profiles)
  ):
    raise ValueError(
        'strat_labels must be None, a dict, or a list of length num_profiles'
        ' ({}). Got length {}.'.format(num_profiles, len(strat_labels))
    )

  pi_list = np.empty((num_profiles, 0))
  pi, alpha, m = None, None, None  # Unused in infinite-alpha regime
  epsilon_list = []
  epsilon_pi_hist = {}
  num_iters = 0

  epsilon_mult_factor = 0.5
  alpharank_succeeded_once = False

  if warm_start_epsilon is not None:
    epsilon = warm_start_epsilon
  else:
    epsilon = 0.5

  while True:
    try:
      pi_prev = pi
      _, _, pi, _, _ = compute(payoff_tables, m=m, alpha=alpha,
                               use_inf_alpha=True, inf_alpha_eps=epsilon)
      epsilon_pi_hist[epsilon] = pi
      # Stop when pi converges
      if num_iters > min_iters and np.allclose(pi, pi_prev):
        break

      epsilon *= epsilon_mult_factor
      num_iters += 1
      alpharank_succeeded_once = True
      if num_iters >= max_iters:
        raise RuntimeError(
            'AlphaRank stationary distribution not found after {} iterations '
            'of pi_vs_epsilon sweep'.format(num_iters)
        )

    except ValueError as value_error:
      print('Error: ', value_error, epsilon, min_epsilon)
      # Case where epsilon has been decreased beyond desirable limits but no
      # distribution found.
      if epsilon < min_epsilon:
        raise RuntimeError(
            'AlphaRank stationary distribution not found and '
            'epsilon < min_epsilon.'
        ) from value_error
      # Case where epsilon >= min_epsilon, but still small enough that it causes
      # causes exceptions due to precision issues. So increase it.
      epsilon /= epsilon_mult_factor

      # Case where alpharank_succeeded_once (i.e., epsilon_list and pi_list have
      # at least one entry), and a) has not converged yet and b) failed on this
      # instance due to epsilon being too small. I.e., the rate of decreasing
      # of epsilon is too high.
      if alpharank_succeeded_once:
        epsilon_mult_factor = (epsilon_mult_factor+1.)/2.
        epsilon *= epsilon_mult_factor

  epsilon_list, pi_list = zip(*[(epsilon, epsilon_pi_hist[epsilon])
                                for epsilon in sorted(epsilon_pi_hist.keys(),
                                                      reverse=True)])
  pi_list = np.asarray(pi_list)

  if visualize:
    if strat_labels is None:
      strat_labels = utils.get_strat_profile_labels(payoff_tables,
                                                    payoffs_are_hpt_format)
    alpharank_visualizer.plot_pi_vs_alpha(
        pi_list.T,
        epsilon_list,
        num_populations,
        num_strats_per_population,
        strat_labels,
        num_strats_to_label=num_strats_to_label,
        legend_sort_clusters=legend_sort_clusters,
        xlabel=r'Infinite-AlphaRank Noise $\epsilon$')

  if return_epsilon:
    return pi_list[-1], epsilon_list[-1]
  else:
    return pi_list[-1]

