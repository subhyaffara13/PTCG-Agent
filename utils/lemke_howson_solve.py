
def lemke_howson_solve(row_payoffs, col_payoffs):
  """Find Nash equilibria using the Lemke-Howson algorithm.

  The algorithm is not guaranteed to find all equilibria. Also it can yield
  wrong answers if the game is degenerate (but raises warnings in that case).
  Args:
    row_payoffs: payoffs for row player
    col_payoffs: payoffs for column player
  Yields:
    (row_mixture, col_mixture), numpy vectors of float64s.
  """

  showwarning = warnings.showwarning
  warned_degenerate = [False]

  def showwarning_check_degenerate(message, *args, **kwargs):
    if "Your game could be degenerate." in str(message):
      warned_degenerate[0] = True
    showwarning(message, *args, **kwargs)

  try:
    warnings.showwarning = showwarning_check_degenerate
    for row_mixture, col_mixture in nashpy.Game(
        row_payoffs, col_payoffs).lemke_howson_enumeration():
      if warned_degenerate[0]:
        # attempt to discard obviously-wrong results
        if (row_mixture.shape != row_payoffs.shape[:1] or
            col_mixture.shape != row_payoffs.shape[1:]):
          warnings.warn("Discarding ill-shaped solution.")
          continue
        if (not np.isfinite(row_mixture).all() or
            not np.isfinite(col_mixture).all()):
          warnings.warn("Discarding non-finite solution.")
          continue
      yield row_mixture, col_mixture
  finally:
    warnings.showwarning = showwarning

