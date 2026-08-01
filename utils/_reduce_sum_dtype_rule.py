
def _reduce_sum_dtype_rule(operand, *, axes, **_):
  dt = _reduce_number_dtype_rule('reduce_sum', operand)
  if (operand.dtype in [np.float16, dtypes.bfloat16] and
      not config.allow_f16_reductions.value and
      not all(core.definitely_equal(operand.shape[d], 1) for d in axes)):
    raise ValueError(f"reduce_sum on operand {operand.str_short(True)} is not "
                     "allowed when jax_allow_f16_reductions=False.")
  return dt

