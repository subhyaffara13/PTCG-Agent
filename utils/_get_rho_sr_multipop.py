
def _get_rho_sr_multipop(payoff_table_k,
                         payoffs_are_hpt_format,
                         k,
                         m,
                         r,
                         s,
                         alpha,
                         use_fast_compute=True):
  """Gets fixation probability for multi-population games.

  Specifically, considers the fitnesses of two strategy profiles r and s given
  the payoff table of the k-th population. Profile s is the current profile and
  r is a mutant profile. Profiles r and s are identical except for the k-th
  element, which corresponds to the deviation of the k-th population's
  monomorphic strategy from s[k] to r[k].

  Args:
    payoff_table_k: The k-th population's payoff table.
    payoffs_are_hpt_format: Boolean indicating whether payoff_table_k is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT), or numpy
      array. True indicates HPT format, False indicates numpy array.
    k: Index of the k-th population.
    m: Total number of agents in the k-th population.
    r: Strategy profile containing mutant strategy r for population k.
    s: Current strategy profile.
    alpha: Fermi distribution temperature parameter.
    use_fast_compute: Boolean indicating whether closed-form computation should
      be used.

  Returns:
    Probability of strategy r fixating in population k.
  """
  # Fitnesses are not dependent on population sizes for multipopulation case, so
  # can be computed outside the loops
  # Fitness of population k agent given strategy profile r
  f_r = _get_payoff(payoff_table_k, payoffs_are_hpt_format, r, k)
  # Fitness of population k agent given strategy profile s
  f_s = _get_payoff(payoff_table_k, payoffs_are_hpt_format, s, k)

  if use_fast_compute:
    u = alpha * (f_r - f_s)
    if np.isclose(u, 0, atol=1e-14):
      # To avoid divide by 0, use first-order approximation when u is near 0
      result = 1 / m
    else:
      result = (1 - np.exp(-u)) / (1 - np.exp(-m * u))
  else:
    summed = 0
    for l in range(1, m):
      t_mult = 1.
      for p_r in range(1, l + 1):  # pylint: disable= unused-variable
        t_mult *= np.exp(-alpha * (f_r - f_s))
      summed += t_mult
    result = (1 + summed)**(-1)

  return result

