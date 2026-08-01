
def _permutation(key, x, axis, independent):
  if independent or np.ndim(x) == 1:
    return _shuffle(key, x, axis)
  ind = _shuffle(key, jnp.arange(x.shape[axis]), 0)
  return jnp.take(x, ind, axis, unique_indices=True)

