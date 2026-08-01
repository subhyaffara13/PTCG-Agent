
def scale_by_shape(
    weight_dimension_numbers: WeightDimNumOrFn | None = None,
    consistent_rms: jax.typing.ArrayLike | None = None,
) -> base.GradientTransformation:
  """Scale updates by factors derived from parameter shape.

  Args:
    weight_dimension_numbers: An optional tree with the same structure as the
      params of `MuonDimensionNumbers`s, specifying how to reshape the
      parameters before and after the orthogonalization OR a callable returning
      such a tree. None implies that all parameters are 2D matrices.
    consistent_rms: An optional float to activate consistent RMS scaling.
      If float, scales updates by `sqrt(max(fan_in, fan_out)) * consistent_rms`.
      If None, uses width scaling `sqrt(max(1, fan_out / fan_in))`.

  Returns:
    A `GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params
    if callable(weight_dimension_numbers):
      # Populate weight_dim_nums if it's a callable. Use updates instead of
      # actual params since only shapes matter and params may not be provided.
      resolved_weight_dim_nums = weight_dimension_numbers(updates)
    else:
      resolved_weight_dim_nums = weight_dimension_numbers

    if consistent_rms is not None:
      scaling_fn = functools.partial(
          _scale_update_for_consistent_rms, consistent_rms=consistent_rms
      )
    else:
      scaling_fn = _scale_update_for_width_transfer

    scaled_updates = jax.tree.map(
        scaling_fn,
        updates,
        resolved_weight_dim_nums,
        is_leaf=_is_weight_dim_nums,
    )
    return scaled_updates, state

  # Use the standard empty_state initializer, as this transform is stateless
  return base.GradientTransformation(base.init_empty_state, update_fn)

