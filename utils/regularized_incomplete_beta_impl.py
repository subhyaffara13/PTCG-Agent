
def regularized_incomplete_beta_impl(a, b, x, *, dtype):
  shape = a.shape

  def nth_partial_betainc_numerator(iteration, a, b, x):
    """
    The partial numerator for the incomplete beta function is given
    here: http://dlmf.nist.gov/8.17.E23 Note that there is a special
    case: the partial numerator for the first iteration is one.
    """
    iteration_bcast = broadcast_in_dim(iteration, shape, [])
    iteration_is_even = eq(iteration_bcast % full_like(iteration_bcast, 2),
                           full_like(iteration_bcast, 0))
    iteration_is_one = eq(iteration_bcast, full_like(iteration_bcast, 1))
    iteration_minus_one = iteration_bcast - full_like(iteration_bcast, 1)
    m = iteration_minus_one // full_like(iteration_minus_one, 2)
    m_is_zero = eq(m, full_like(m, 0))
    m = convert_element_type(m, dtype)
    one = full_like(a, 1)
    two = full_like(a, 2.0)
    # Partial numerator terms

    # When a is close to zero and m == 0, using zero_numerator avoids
    # inaccuracies when FTZ or DAZ is enabled:
    zero_numerator = -(a + b) * x / (a + one)
    even_numerator = select(m_is_zero, zero_numerator,
                            -(a + m) * (a + b + m) * x / (
                              (a + two * m) * (a + two * m + one)))
    odd_numerator = m * (b - m) * x / ((a + two * m - one) * (a + two * m))
    one_numerator = full_like(x, 1.0)
    numerator = select(iteration_is_even, even_numerator, odd_numerator)
    return select(iteration_is_one, one_numerator, numerator)

  def nth_partial_betainc_denominator(iteration, a, b, x):
    iteration_bcast = broadcast_in_dim(iteration, shape, [])
    return select(eq(iteration_bcast, full_like(iteration_bcast, 0)),
                  full_like(x, 0), full_like(x, 1))

  a_is_zero = bitwise_or(eq(a, full_like(a, 0)), eq(b, full_like(b, float('inf'))))
  b_is_zero = bitwise_or(eq(b, full_like(b, 0)), eq(a, full_like(a, float('inf'))))
  x_is_zero = eq(x, full_like(x, 0))
  x_is_one = eq(x, full_like(x, 1))
  x_is_not_zero = bitwise_not(x_is_zero)
  x_is_not_one = bitwise_not(x_is_one)
  is_nan = bitwise_or(bitwise_or(_isnan(a), _isnan(b)), _isnan(x))

  result_is_zero = bitwise_or(bitwise_and(b_is_zero, x_is_not_one), bitwise_and(a_is_zero, x_is_zero))
  result_is_one = bitwise_or(bitwise_and(a_is_zero, x_is_not_zero), bitwise_and(b_is_zero, x_is_one))

  result_is_nan = bitwise_or(bitwise_or(bitwise_or(
    lt(a, full_like(a, 0)), lt(b, full_like(b, 0))),
    lt(x, full_like(x, 0))), gt(x, full_like(x, 1)))
  result_is_nan = bitwise_or(result_is_nan, bitwise_or(bitwise_and(a_is_zero, b_is_zero), is_nan))

  # The continued fraction will converge rapidly when x <
  # (a+1)/(a+b+2) as per: http://dlmf.nist.gov/8.17.E23.
  #
  # Otherwise, we can rewrite using the symmetry relation as per:
  # http://dlmf.nist.gov/8.17.E4
  converges_rapidly = lt(x, (a + full_like(a, 1)) / (a + b + full_like(b, 2.0)))
  a_orig = a
  a = select(converges_rapidly, a, b)
  b = select(converges_rapidly, b, a_orig)
  x = select(converges_rapidly, x, sub(full_like(x, 1), x))

  continued_fraction = lentz_thompson_barnett_algorithm(
    num_iterations=200 if dtype == np.float32 else 600,
    small=(dtypes.finfo(dtype).eps / 2).astype(dtype),
    threshold=(dtypes.finfo(dtype).eps / 2).astype(dtype),
    nth_partial_numerator=nth_partial_betainc_numerator,
    nth_partial_denominator=nth_partial_betainc_denominator,
    inputs=[a, b, x]
  )

  # For very small a and to avoid division by zero, we'll use
  # a * gamma(a) = gamma(a + 1) -> 1 as a -> 0+.
  very_small = (dtypes.finfo(dtype).tiny * 2).astype(dtype)
  lbeta_ab_small_a = lgamma(b) - lgamma(a + b)
  lbeta_ab = lgamma(a) + lbeta_ab_small_a
  factor = select(lt(a, full_like(a, very_small)),
                  exp(log1p(-x) * b - lbeta_ab_small_a),
                  exp(log(x) * a + log1p(-x) * b - lbeta_ab) / a)
  result = continued_fraction * factor
  result = select(converges_rapidly, result, sub(full_like(result, 1), result))

  result = select(result_is_zero, full_like(a, 0), result)
  result = select(result_is_one, full_like(a, 1), result)
  result = select(result_is_nan, full_like(a, float('nan')), result)
  return result

