
def _normalize_axes(axis, ndim):
    axes = []
    if ndim == 0 and axis:
        # Better error message in this case
        raise IndexError(f"Dimension out of range: {axis[0]}")
    lower, upper = -ndim, ndim - 1
    for a in axis:
        if a < lower or a > upper:
            # Match torch error message (e.g., from sum())
            raise IndexError(f"Dimension out of range (expected to be in range of [{lower}, {upper}], but got {a}")
        if a < 0:
            a = a + ndim
        if a in axes:
            # Use IndexError instead of RuntimeError, and "axis" instead of "dim"
            raise IndexError(f"Axis {a} appears multiple times in the list of axes")
        axes.append(a)
    return sorted(axes)


def _normalize_axes(
    x: jax.Array, dim_nums: GaLoreDimensionNumbers
) -> tuple[tuple[int, ...], tuple[int, ...]]:
  """Normalize axes in dimension numbers to tuples of non-negative ints."""
  if isinstance(dim_nums.reduction_axis, int):
    reduction_axes = (dim_nums.reduction_axis % x.ndim,)
  else:
    reduction_axes = tuple(ax % x.ndim for ax in dim_nums.reduction_axis)

  if isinstance(dim_nums.output_axis, int):
    output_axes = (dim_nums.output_axis % x.ndim,)
  else:
    output_axes = tuple(ax % x.ndim for ax in dim_nums.output_axis)

  return reduction_axes, output_axes


def _normalize_axes(x: jax.Array, dim_nums: MuonDimensionNumbers) -> tuple[
    tuple[int, ...], tuple[int, ...]]:
  """Normalize axes in dimension numbers to two tuples of non-negative ints."""
  if isinstance(dim_nums.reduction_axis, int):
    dim_nums = dim_nums._replace(reduction_axis=(dim_nums.reduction_axis,))
  reduction_axes = tuple(ax % x.ndim for ax in dim_nums.reduction_axis)

  if isinstance(dim_nums.output_axis, int):
    dim_nums = dim_nums._replace(output_axis=(dim_nums.output_axis,))
  output_axes = tuple(ax % x.ndim for ax in dim_nums.output_axis)
  return reduction_axes, output_axes


def _normalize_axes(axes: tuple[int, ...], ndim: int) -> tuple[int, ...]:
  # A tuple by convention. len(axes_tuple) then also gives the rank efficiently.
  return tuple(sorted(ax if ax >= 0 else ndim + ax for ax in axes))


def _normalize_axes(axes: tuple[int, ...], ndim: int) -> tuple[int, ...]:
  # A tuple by convention. len(axes_tuple) then also gives the rank efficiently.
  return tuple(sorted(ax if ax >= 0 else ndim + ax for ax in axes))


def _normalize_axes(axes, ndim):
  # A tuple by convention. len(axes_tuple) then also gives the rank efficiently.
  return tuple(ax if ax >= 0 else ndim + ax for ax in axes)

