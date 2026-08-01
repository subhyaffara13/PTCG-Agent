
def _swap(f, i):
    """
    Make the variable `x_i` the leading one in a multivariate polynomial `f`.
    """
    ring = f.ring
    fswap = ring.zero
    for monom, coeff in f.iterterms():
        monomswap = (monom[i],) + monom[:i] + monom[i+1:]
        fswap[monomswap] = coeff
    return fswap


def _swap(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    transforms,
    val: jax.Array,
    mask: jax.Array | None,
    *,
    clock=None,
    increment_clock: bool = True,
    source_info=None,
) -> tuple[jax.Array, jax.Array]:
  """Performs a swap into the buffer for `allocation_key` from the given device and thread."""
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = tuple(int(x) for x in grid_point_coords)
  thread_id_as_int = int(thread_id)
  allocation_key = HostAllocationKey.from_array(allocation_key_as_array)
  del device_id, thread_id, allocation_key_as_array

  transforms = _remove_noop_transforms(transforms)
  _validate_transforms(transforms)
  transforms = jax.tree.map(int, transforms)

  if mask is not None:
    assert mask.shape == val.shape

  shared_memory = _get_shared_memory()

  global_thread_id = shared_memory.get_global_thread_id(
      device_id_as_int, thread_id_as_int
  )

  read_write_range = interpret_utils.to_range(transforms)
  ret, (shape, _), clock_ = shared_memory.swap_buffer_content(
      allocation_key,
      read_write_range,
      np.array(val),
      np.array(mask) if mask is not None else None,
      global_thread_id,
      increment_clock=increment_clock,
      logging_info=interpret_utils.GPULoggingInfo(
          device_id=device_id_as_int,
          grid_point_coords=grid_point_coords_as_tuple,
          thread_id=thread_id_as_int,
          source_info=source_info,
      ),
  )
  clock = clock if clock is not None else clock_

  if ret is None:
    if mask is None:
      raise ValueError(
          f"Out-of-bounds swap of {allocation_key}:"
          f" swapping [{read_write_range}] but buffer has shape"
          f" {shape} ."
      )
    else:
      # TODO(jburnim): Include indices of out-of-bounds locations where mask
      # is True.
      raise ValueError(
          f"Out-of-bounds masked swap of {allocation_key}: swapping"
          f" [{read_write_range}] but buffer has shape {shape} . "
      )

  if shared_memory.detect_races:
    get_races().check_write(
        device_id_as_int,
        thread_id_as_int,
        clock,
        allocation_key,
        read_write_range,
        source_info=source_info,
    )
  return token, jnp.array(ret)

