
def _array_to_2d_tile_array(
    x: jax_typing.Array, tiling: tuple[int, ...]
) -> np.ndarray:
  t1, t2 = tiling[-2:]
  tiled_shape = tuple(x.shape[i] // tiling[i] for i in range(len(x.shape)))
  # Allocate an empty object array to ensure Numpy doesn't coerce JAX tracers
  tiles = np.empty(tiled_shape, dtype=object)
  for idx in np.ndindex(*tiled_shape):
    *leading, i1, i2 = idx
    slices = tuple(leading) + (
        slice(i1 * t1, (i1 + 1) * t1),
        slice(i2 * t2, (i2 + 1) * t2),
    )
    # Standard Integer indexing inherently drops the outer dims -> returns strict 2D array
    tiles[idx] = x[slices]
  return tiles

