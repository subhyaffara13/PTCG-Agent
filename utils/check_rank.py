
def check_rank(array: jax.typing.ArrayLike, rank: int):
  """Check that `array` has the specified rank."""
  shape = array.shape if hasattr(array, 'shape') else np.asarray(array).shape
  array_rank = len(shape)
  if array_rank != rank:
    raise ValueError(
        f'Expected the input to have rank {rank}, got {array_rank} instead'
    )

