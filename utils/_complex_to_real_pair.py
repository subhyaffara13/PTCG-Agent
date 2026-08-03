from typing import Union

def _complex_to_real_pair(
    x: jax.typing.ArrayLike,
) -> Union[jax.typing.ArrayLike, SplitRealAndImaginaryArrays]:
  """Splits a complex array into a `SplitRealAndImaginaryArrays`.

  Args:
    x: The input array, can be complex or real.

  Returns:
    `SplitRealAndImaginaryArrays` if the input is a complex array. If the
    input is a real array, it is passed through unmodified.
  """
  if jnp.iscomplexobj(x):
    return SplitRealAndImaginaryArrays(x.real, x.imag)
  else:
    return x

