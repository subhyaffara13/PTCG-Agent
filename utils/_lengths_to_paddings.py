
def _lengths_to_paddings(
    lengths: jax.typing.ArrayLike, maxlength: int) -> np.ndarray:
  indices = jnp.arange(maxlength).reshape((1,) * lengths.ndim + (maxlength,))  # pytype: disable=attribute-error  # jax-arraylike   # noqa: E501
  lengths = jnp.expand_dims(lengths, axis=-1)
  elem_valid = indices < lengths
  return np.logical_not(elem_valid).astype(np.float32)

