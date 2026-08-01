
def sort_key_val(keys, values, dimension=-1):
  idxs = list(np.ix_(*[np.arange(d) for d in keys.shape]))
  idxs[dimension] = np.argsort(keys, axis=dimension)
  return keys[tuple(idxs)], values[tuple(idxs)]


def sort_key_val(keys: Array, values: ArrayLike, dimension: int = -1,
                 is_stable: bool = True) -> tuple[Array, Array]:
  """Sorts ``keys`` along ``dimension`` and applies the same permutation to ``values``."""
  dimension = canonicalize_axis(dimension, len(keys.shape))
  k, v = sort_p.bind(keys, values, dimension=dimension, is_stable=is_stable, num_keys=1)
  return k, v


def sort_key_val(
    keys: jax.Array, values: jax.Array, *,
    mask: jax.Array | None = None, descending: bool = False
) -> jax.Array:
  """Sorts keys and values, pushing invalid elements to the last positions.

  Args:
    keys: An array of integers or floats.
    values: An array of values corresponding to the keys.
    mask: An optional array of booleans, which specifies which elements of
      `keys` and `values` are valid. If `None`, all elements are valid.
    descending: Whether to sort in descending order.

  Returns:
    sorted_keys, sorted_values, [output_mask]: The sorted keys and values, and,
    if a mask was given, the corresponding mask for output keys and values.
  """
  maybe_mask = () if mask is None else (mask,)
  return masked_sort_p.bind(keys, values, *maybe_mask, descending=descending)

