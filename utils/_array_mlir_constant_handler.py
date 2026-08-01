
def _array_mlir_constant_handler(val, aval):
  try:
    return mlir.ir_constant(val._value)
  except RuntimeError as e:
    # TODO(yashkatariya): Ideally we would catch a custom exception from
    # `_value` function in ArrayImpl instead of checking the error string.
    if 'Fetching value for `jax.Array` that spans non-addressable' in str(e):
      raise RuntimeError(
          "Closing over jax.Array that spans non-addressable (non process"
          " local) devices is not allowed. Please pass such arrays as arguments"
          f" to the function. Got jax.Array: {val.aval.str_short()}") from e
    raise

