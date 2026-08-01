
def lentz_thompson_barnett_algorithm(*,num_iterations, small, threshold, nth_partial_numerator, nth_partial_denominator, inputs):
  # Position in the evaluation.
  kIterationIdx = 0
  # Whether or not we have reached the desired tolerance.
  kValuesUnconvergedIdx = 1
  # Ratio between nth canonical numerator and the nth-1 canonical numerator.
  kCIdx = 2
  # Ratio between nth-1 canonical denominator and the nth canonical denominator.
  kDIdx = 3
  # Computed approximant in the evaluation.
  kHIdx = 4

  def while_cond_fn(values):
    iteration = values[kIterationIdx]
    iterations_remain_cond = lt(iteration, num_iterations)
    values_unconverged_cond = values[kValuesUnconvergedIdx]
    return bitwise_and(iterations_remain_cond, values_unconverged_cond)

  def while_body_fn(values):
    iteration = values[kIterationIdx]
    partial_numerator = nth_partial_numerator(iteration, *inputs)
    partial_denominator = nth_partial_denominator(iteration, *inputs)

    c = add(partial_denominator, div(partial_numerator, values[kCIdx]))
    small_constant = full_like(c, small)
    c = select(lt(abs(c), small_constant), small_constant, c)
    d = add(partial_denominator, mul(partial_numerator, values[kDIdx]))
    d = select(lt(abs(d), small_constant), small_constant, d)
    d = reciprocal(d)
    delta = mul(c, d)
    h = mul(values[kHIdx], delta)

    # Update values
    values[kIterationIdx] = iteration + 1
    values[kCIdx] = c
    values[kDIdx] = d
    values[kHIdx] = h
    # If any values are greater than the tolerance, we have not converged.
    tolerance_comparison = ge(abs(sub(delta, _const(delta, 1.0))), threshold)
    values[kValuesUnconvergedIdx] = _any(tolerance_comparison)
    return values

  partial_denominator = nth_partial_denominator(0, *inputs)
  h = select(lt(abs(partial_denominator), small),
             broadcast_in_dim(small, partial_denominator.shape, ()),
             partial_denominator)
  values = [1,True,h,full_like(h,0),h]
  values = while_loop(while_cond_fn, while_body_fn, values)
  return values[kHIdx]

