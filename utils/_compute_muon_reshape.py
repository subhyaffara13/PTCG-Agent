import math


def _compute_muon_reshape(x: jax.Array, dim_nums: MuonDimensionNumbers
                          ) -> tuple[ReshapeFn, ReshapeFn]:
  """Compute the reshape and inverse functions for an array from a spec."""
  if x.ndim < 2:
    raise ValueError('Muon optimized parameters must have rank >= 2, got'
                     f' {x.ndim=}')
  reduction_axes, output_axes = _normalize_axes(x, dim_nums)
  if set(reduction_axes) & set(output_axes):
    raise ValueError('Normalized reduction axes and output axes must be'
                     f' disjoint, got {reduction_axes} and {output_axes}.'
                     f' Originally {dim_nums=} and {x.shape=}')
  batch_axes = tuple(sorted(set(range(x.ndim)) - set(reduction_axes)
                            - set(output_axes)))
  transpose = batch_axes + reduction_axes + output_axes
  inv_transpose = tuple(sorted(range(x.ndim), key=lambda i: transpose[i]))
  axes2shape = lambda axes: tuple(x.shape[ax] for ax in axes)
  # Reshape to (batch, reduction, output) to match the (reduction, output)
  # structure of the original muon for 2D weights.
  flat_shape = (
      math.prod(axes2shape(batch_axes)),
      math.prod(axes2shape(reduction_axes)),
      math.prod(axes2shape(output_axes)),
  )
  unflat_shape = (
      axes2shape(batch_axes)
      + axes2shape(reduction_axes)
      + axes2shape(output_axes)
  )
  reshape_fn = lambda x: x.transpose(transpose).reshape(flat_shape)
  inverse_fn = lambda x: x.reshape(unflat_shape).transpose(inv_transpose)
  return reshape_fn, inverse_fn

