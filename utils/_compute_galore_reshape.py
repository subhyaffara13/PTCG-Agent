import math


def _compute_galore_reshape(
    x: jax.Array, dim_nums: GaLoreDimensionNumbers
) -> tuple[ReshapeFn, ReshapeFn]:
  """Compute reshape functions for treating a tensor as a 2D matrix.

  Args:
    x: The tensor to reshape.
    dim_nums: Specification for which axes form the matrix.

  Returns:
    A tuple of (reshape_fn, inverse_fn) where:
    - reshape_fn: transforms x to shape (reduction_size, output_size)
    - inverse_fn: transforms back to original shape
  """
  if x.ndim < 2:
    raise ValueError(
        f"GaLore requires tensors with rank >= 2, got shape {x.shape}"
    )

  reduction_axes, output_axes = _normalize_axes(x, dim_nums)

  if set(reduction_axes) & set(output_axes):
    raise ValueError(
        f"Reduction axes {reduction_axes} and output axes {output_axes} "
        f"must be disjoint. Got dim_nums={dim_nums} for shape {x.shape}"
    )

  # Any axes not in reduction or output are batch axes (should be empty for
  # typical usage, but we handle it for completeness)
  all_specified = set(reduction_axes) | set(output_axes)
  if len(all_specified) != x.ndim:
    raise ValueError(
        f"All axes must be specified. Got reduction={reduction_axes}, "
        f"output={output_axes} for tensor with {x.ndim} dimensions"
    )

  # Compute transpose to put reduction axes first, then output axes
  transpose = reduction_axes + output_axes
  inv_transpose = tuple(sorted(range(x.ndim), key=lambda i: transpose[i]))

  axes2shape = lambda axes: tuple(x.shape[ax] for ax in axes)
  reduction_size = math.prod(axes2shape(reduction_axes))
  output_size = math.prod(axes2shape(output_axes))

  transposed_shape = axes2shape(reduction_axes) + axes2shape(output_axes)

  reshape_fn = lambda y: y.transpose(transpose).reshape(
      reduction_size, output_size
  )
  inverse_fn = lambda y: y.reshape(transposed_shape).transpose(inv_transpose)

  return reshape_fn, inverse_fn

