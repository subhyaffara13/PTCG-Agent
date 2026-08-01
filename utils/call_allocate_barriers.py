
def call_allocate_barriers(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    axes_dims: tuple[int, ...],
    num_arrivals: jax.Array,
    num_barriers: jax.Array,
    ref_count: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
) -> tuple[jax.Array, jax.Array]:
  shape_and_dtype = HostAllocationKey.shape_and_dtype()
  result_shape = (num_barriers, *shape_and_dtype.shape)
  result_shape_and_dtype = jax.ShapeDtypeStruct(
      result_shape, shape_and_dtype.dtype
  )
  return callback.io_callback(
      functools.partial(
          _allocate_barriers,
          source_info=source_info,
          axes_dims=axes_dims,
      ),
      (TOKEN_SHAPE_DTYPE, result_shape_and_dtype),
      token=token,
      device_id=device_id,
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      num_arrivals=num_arrivals,
      num_barriers=num_barriers,
      ref_count=ref_count,
  )

