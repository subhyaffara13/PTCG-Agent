
def _multinomial_coefficients(distributions):
  """Returns the multinomial coefficients.

  Args:
    distributions: The distributions table [num_rows, num_strategies].
  """
  v_factorial = np.vectorize(math.factorial)
  # Multinomial coefficients (one per distribution Ni).
  # (         P         )
  # ( Ni1, Ni1, ... Nik )
  coefficients = (
      v_factorial(np.sum(distributions, axis=1)) /
      np.prod(v_factorial(distributions), axis=1))

  return coefficients

