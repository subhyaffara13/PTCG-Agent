
def _real_pair_to_complex(
    x: Union[jax.typing.ArrayLike, SplitRealAndImaginaryArrays],
) -> jax.typing.ArrayLike:
  """Merges a `SplitRealAndImaginaryArrays` into a complex array.

  Args:
    x: The input `SplitRealAndImaginaryArrays` or array.

  Returns:
    A complex array obtained from the real and imaginary parts of the
    `SplitRealAndImaginaryArrays`. If the input is not a
    `SplitRealAndImaginaryArrays`, it is passed through unmodified.
  """
  if isinstance(x, SplitRealAndImaginaryArrays):
    return x.real + x.imaginary * 1j
  else:
    return x

