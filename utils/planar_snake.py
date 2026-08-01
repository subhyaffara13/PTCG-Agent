
def planar_snake(
    lin_idx: jax.Array,
    shape: tuple[int | jax.Array, int | jax.Array],
    minor_dim: int,
    tile_width: int,
):
  """Converts a linear index into an index into shape, trying to optimize locality.

  The "space filling curve" this function computes splits the minor dimension
  into tiles of length ``tile_width``. Every other tile has its major dimension
  inverted, so that the iteration order "snakes around" when going from one tile
  to another.

  For a shape of (8, 8), ``minor_dim=0`` and ``tile_width=2``, the iteration
  order is::

       0   2   4   6   8  10  12  14
       1   3   5   7   9  11  13  15
      30  28  26  24  22  20  18  16
      31  29  27  25  23  21  19  17
      32  34  36  38  40  42  44  46
      33  35  37  39  41  43  45  47
      62  60  58  56  54  52  50  48
      63  61  59  57  55  53  51  49

  Notice how each pair of rows forms a tile (``minor_dim=0``, ``tile_width=2``)
  and when moving from one tile to another, the indices increase along columns
  in one of them and decrease in the other.
  """
  tile_width = jnp.int32(tile_width)  # pyrefly: ignore[bad-assignment]
  major_size = jnp.int32(shape[1 - minor_dim])
  minor_size = jnp.int32(shape[minor_dim])

  minor_tile_idx = lax.div(lin_idx, tile_width * major_size)

  def tile_coordinates(lin_idx, width):
    # if minor_dim == 0 then tiles are (tile_width, major_size) else (major_size, tile_width)
    minor_within_tile = lax.rem(lin_idx, width)
    major_within_tile = lax.rem(lax.div(lin_idx, width), major_size)
    minor = minor_tile_idx * tile_width + minor_within_tile
    major = lax.select(
        lax.rem(minor_tile_idx, jnp.int32(2)) == 0,
        major_within_tile,
        major_size - 1 - major_within_tile,
    )
    return (minor, major) if minor_dim == 0 else (major, minor)

  num_full_tiles = minor_size // tile_width
  full_tiles_minor_size = num_full_tiles * tile_width
  num_full_tiles_elements = num_full_tiles * tile_width * major_size
  is_full_tile = lin_idx < num_full_tiles_elements
  return jax.tree.map(
      functools.partial(jax.lax.select, is_full_tile),
      tile_coordinates(lin_idx, tile_width),
      tile_coordinates(lin_idx - num_full_tiles_elements, minor_size - full_tiles_minor_size)
  )

