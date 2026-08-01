
def power_method(w_nus):
  """Quick implementation of the power method.

  Args:
    w_nus:

  Returns:
    Highest eigenvalue of the system.

  Raises:
    ValueError: when the power method did not converge after 10.000 trials.
  """
  p = np.ones(len(w_nus))
  pprime = np.dot(p, w_nus)
  n_trials = 10000
  i = 0
  while np.sum(np.abs(pprime - p)) > 1e-8 and i < n_trials:
    p = pprime
    pprime = np.dot(p, w_nus)
    pprime[pprime < 0] = 0.0
    pprime /= np.sum(pprime)
    i += 1

  if np.sum(np.abs(pprime - p)) > 1e-8 and i >= n_trials:
    raise ValueError(
        "Power method did not converge after {} trials.".format(n_trials)
    )

  p[p < 0] = 0.0
  return p / np.sum(p)

