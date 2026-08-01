
def _2d_tile_array_to_array(tiles: np.ndarray) -> jax_typing.Array:
  raw_arrays = np.empty(tiles.shape, dtype=object)
  for idx in np.ndindex(*tiles.shape):
    raw_arrays[idx] = tiles[idx]
  return jnp.block(raw_arrays.tolist())

