
def _lstm_cudnn_allow_tf32(precision: lax.PrecisionLike) -> bool:
  # the logic from canonicalize_precision that we require here boils down to:
  #
  #   if precision is None and config.jax_default_matmul_precision is not None:
  #     precision = Precision(config.jax_default_matmul_precision)
  #   else:
  #     precision = None
  #
  # but we prefer to still invoke it here for consistency
  precision = lax.canonicalize_precision(precision)
  if precision is None or not (isinstance(precision, tuple) and len(precision) == 2):
    return True
  # cuDNN allows only one precision specifier per RNN op
  match precision:
    case (lax.Precision.HIGHEST, _):
      return False
    case (lax.Precision.HIGH, _):
      return True
    case (lax.Precision.DEFAULT, _): # bfloat16
      raise NotImplementedError("bfloat16 support not implemented for LSTM")
    case _:
      raise ValueError(f"Unexpected precision specifier value {precision}")

