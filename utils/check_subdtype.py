
def check_subdtype(array: jax.typing.ArrayLike, subdtype: jax.typing.DTypeLike):
  """Check that `array`'s dtype is a subdtype of `subdtype`."""
  dtype = jax.dtypes.result_type(array)
  if not jnp.issubdtype(dtype, subdtype):
    raise TypeError(
        f'Expected the input to have a dtype that is a subdtype of {subdtype}, '
        f'got {dtype} instead'
    )

