
def tile_strides(
    strides: tuple[int, ...], tiling: tuple[int, ...]
) -> tuple[int, ...]:
  """Tiles the trailing strides in `strides` according to `tiling`.

  The `len(tiling)` trailing strides in `strides` must be the `len(tiling)`
  smallest strides in `strides`. The same property holds in the result, i.e.,
  given two tiles with indices i and j (i < j) with strides tiled according to
  this function, then all the elements in tile i are physically ordered before
  all the elements in tile j.

  E.g., tile_strides((2048, 32, 1), (8, 4)) = (2048, 256, 32, 4, 1)
  """
  if len(strides) < len(tiling):
    raise ValueError(f"Strides {strides} have lower rank than tiling {tiling}")
  ordered_strides = sorted(strides, reverse=True)
  if set(ordered_strides[-len(tiling):]) != set(strides[-len(tiling):]):
    raise ValueError(
        "Can not tile strides when tiled dimensions have been transposed with "
        f"untiled dimensions. Strides: {strides}, tiling: {tiling}"
    )
  untiled_strides, tiled_strides = strides[:-len(tiling)], strides[-len(tiling):]

  # Zip the strides and tiling together, in order to sort them together. This
  # allows handling cases where multiple tiling dimensions have the same stride,
  # which can occur with size-1 dimensions.
  tiled_strides_and_tiling: list[tuple[int, int]] = list(
      zip(tiled_strides, tiling, strict=True))
  tiled_ordered_strides_and_tiling = sorted(
      tiled_strides_and_tiling, reverse=True)

  to_ordered = lambda i: tiled_ordered_strides_and_tiling.index(tiled_strides_and_tiling[i])
  from_ordered = lambda i: tiled_strides_and_tiling.index(tiled_ordered_strides_and_tiling[i])

  ordered_tiling = [tiling[from_ordered(i)] for i in range(len(tiling))]
  ordered_tiled_strides = [tiled_strides[from_ordered(i)] for i in range(len(tiling))]

  ordered_tiled_tiling_strides = [1]
  for t in reversed(ordered_tiling):
    ordered_tiled_tiling_strides.append(ordered_tiled_tiling_strides[-1] * t)

  prev_s = ordered_tiled_strides[-1]
  for s, t in zip(ordered_tiled_strides[:-1][::-1], ordered_tiling[1:][::-1], strict=True):
    d = prev_s * t
    prev_s = s
    if s % d != 0:
      raise ValueError(
          f"Stride {s} is not divisible by {d} (tile size = {t}). "
          f"Strides: {strides}, tiling: {tiling}"
      )
    ordered_tiled_tiling_strides.append(s // d * ordered_tiled_tiling_strides[-1])

  ordered_tiled_tiling_strides.reverse()

  return (
      *untiled_strides,
      *[ordered_tiled_tiling_strides[to_ordered(i)] for i in range(len(tiling))],
      *[ordered_tiled_tiling_strides[len(tiling) + to_ordered(i)] for i in range(len(tiling))]
  )

