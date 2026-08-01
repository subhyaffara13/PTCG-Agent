
def _make_round_harness(name,
                        *,
                        shape=(100, 100),
                        dtype=np.float32,
                        rounding_method=lax.RoundingMethod.AWAY_FROM_ZERO,
                        operand=None):
  operand = operand if operand is not None else RandArg(shape, dtype)
  define(
      "round",
      f"{name}_shape={jtu.format_shape_dtype_string(operand.shape, operand.dtype)}_roundingmethod={rounding_method}",
      lax.round, [operand, StaticArg(rounding_method)],
      dtype=dtype,
      operand=operand,
      rounding_method=rounding_method)

