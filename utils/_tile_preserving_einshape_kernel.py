import math


def _tile_preserving_einshape_kernel(
    equation: str, x: jax_typing.Array, **size_vars: int
):
  tiling = tpu_info.infer_tiling(jax_core.typeof(x))
  assert tiling is not None
  t1, t2 = tiling[-2:]

  assert isinstance(t1, int)
  assert isinstance(t2, int)
  dims = _init_dims(x.shape, t1, t2)
  tiles = _array_to_2d_tile_array(x, tiling)  # pyrefly: ignore[bad-argument-type]
  transforms = get_einshape_transforms(equation, x.shape, **size_vars)

  def get_outer_shape(dims_list: list[list[Factor]]) -> tuple[int, ...]:
    return tuple(
        math.prod([f.size for f in d if f.kind == "outer"]) for d in dims_list
    )

  for t in transforms:
    match t:
      case Transpose(permutation):
        tiles = np.transpose(tiles, permutation)
        dims = [dims[i] for i in permutation]
      case SplitDims(index, sizes):
        new_dims = _apply_split(dims[index], sizes)
        assert (
            new_dims is not None
        ), "Tile preserving check passed but split failed."
        dims = dims[:index] + new_dims + dims[index + 1 :]
        tiles = tiles.reshape(get_outer_shape(dims))
      case MergeDims(index, count):
        merged = [b for d in dims[index : index + count] for b in d]
        dims = dims[:index] + [_consolidate(merged)] + dims[index + count :]
        tiles = tiles.reshape(get_outer_shape(dims))

  return _2d_tile_array_to_array(tiles)

