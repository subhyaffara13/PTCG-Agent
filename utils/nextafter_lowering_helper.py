
def nextafter_lowering_helper(x, y):
  if x.dtype != y.dtype:
    raise ValueError(
        "The two inputs to `nextafter` must have the same dtype, but got"
        f" {x.dtype} and {y.dtype}"
    )

  if x.dtype not in (jnp.float32, jnp.float64):
    raise ValueError(
        f"`nextafter` only supports float32 and float64, but got {x.dtype}"
    )

  jnp_float, jnp_uint, np_float, np_uint, np_int = (
      jnp.float32, jnp.uint32, np.float32, np.uint32, np.int32,
  ) if x.dtype == jnp.float32 else (
      jnp.float64, jnp.uint64, np.float64, np.uint64, np.int64,
  )

  bitwidth = dtypes.itemsize_bits(x.dtype)

  x_as_int = x.view(jnp_uint)
  y_as_int = y.view(jnp_uint)

  # The result is NaN if either "x" or "y" are NaN.
  nan_input = jnp.isnan(x) | jnp.isnan(y)
  result_for_nan = jnp.full_like(x_as_int, np_float(np.nan).view(np_uint))

  # The sign bit is the MSB.
  sign_bit = jnp_uint(1 << (bitwidth - 1))
  # Discard the sign bit to make the result non-negative.
  sign_mask = sign_bit
  negated_sign_mask = ~sign_bit
  x_abs = x_as_int & negated_sign_mask
  y_abs = y_as_int & negated_sign_mask

  # When both "x" and "y" are equal, the result is "y".
  x_and_y_are_equal = x == y
  result_for_equal = y_as_int

  # When both "x" and "y" are 0, the result is "y". This is a separate case
  # from above because "x" and "y" might have a different sign.
  zero = jnp.zeros_like(x_as_int)
  x_is_zero = x_abs == zero
  y_is_zero = y_abs == zero
  result_for_both_zero = y_as_int

  x_sign = x_as_int & sign_mask
  y_sign = y_as_int & sign_mask

  # If x == 0 && y != 0, we need to return the smallest subnormal number
  # signed like "y".
  one = jnp.ones_like(x_as_int)
  result_for_x_zero_y_non_zero = y_sign | one

  # If the sign of "x" and "y" disagree:
  # - we need to make the magnitude of "from" smaller so that it is closer to
  #   zero.
  #
  # Otherwise the signs agree:
  # - "x" with a magnitude larger than "y" means we need to make the magnitude
  #   smaller.
  # - "x" with a magnitude smaller than "y" means we need to make the magnitude
  #   larger.
  signs_disagree = x_sign != y_sign
  x_magnitude_larger_than_y = x_abs > y_abs
  result_has_smaller_magnitude = x_magnitude_larger_than_y | signs_disagree
  minus_one = jnp.full_like(x_as_int, np_int(-1).view(np_uint))
  magnitude_adjustment = jnp.where(result_has_smaller_magnitude, minus_one, one)
  result = x_as_int + magnitude_adjustment

  # Handle x == +-0.
  result = jnp.where(
      x_is_zero,
      jnp.where(y_is_zero, result_for_both_zero, result_for_x_zero_y_non_zero),
      result,
  )

  # Handle x == y.
  result = jnp.where(x_and_y_are_equal, result_for_equal, result)

  # Handle isnan(x) || isnan(y).
  result = jnp.where(nan_input, result_for_nan, result)

  # Cast back to the original type.
  return result.view(jnp_float)

