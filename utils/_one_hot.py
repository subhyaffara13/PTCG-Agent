
def _one_hot(x: Array, num_classes: int, *,
             dtype: DTypeLike, axis: int | AxisName) -> Array:
  num_classes = core.concrete_dim_or_error(
      num_classes,
      "The error arose in jax.nn.one_hot argument `num_classes`.")
  try:
    output_pos_axis = util.canonicalize_axis(axis, x.ndim + 1)  # pyrefly: ignore[bad-argument-type]
  except TypeError:
    axis_size = lax.axis_size(axis)
    if num_classes != axis_size:
      raise ValueError(f"Expected num_classes to match the size of axis {axis}, "
                       f"but {num_classes} != {axis_size}") from None
    axis_idx = lax.axis_index(axis)
    return jnp.asarray(x == axis_idx, dtype=dtype)
  assert isinstance(axis, SupportsIndex)
  axis = operator.index(axis)
  lhs = lax.expand_dims(x, (axis,))
  rhs_shape = [1] * x.ndim
  rhs_shape.insert(output_pos_axis, num_classes)
  # TODO(yashkatariya): Maybe expose `out_sharding` on `one_hot` too?
  rhs_sharding = NamedSharding(x.aval.sharding.mesh, P(*[None] * len(rhs_shape)))
  rhs = lax.broadcasted_iota(x.dtype, rhs_shape, output_pos_axis,
                             out_sharding=rhs_sharding)
  return (lhs == rhs).astype(dtype)

