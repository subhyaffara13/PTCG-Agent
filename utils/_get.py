
def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    if (value := d.get(key)) is None:
        return None
    if not isinstance(value, expected_type):
        raise DirectUrlValidationError(
            f"Unexpected type {type(value).__name__} "
            f"(expected {expected_type.__name__})",
            context=key,
        )
    return value


def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    if (value := d.get(key)) is None:
        return None
    if not isinstance(value, expected_type):
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} "
            f"(expected {expected_type.__name__})",
            context=key,
        )
    return value


def _get(ind, seq, default):
    try:
        return seq[ind]
    except (KeyError, IndexError):
        return default


def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    if (value := d.get(key)) is None:
        return None
    if not isinstance(value, expected_type):
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} "
            f"(expected {expected_type.__name__})",
            context=key,
        )
    return value


def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    if (value := d.get(key)) is None:
        return None
    if not isinstance(value, expected_type):
        raise DirectUrlValidationError(
            f"Unexpected type {type(value).__name__} "
            f"(expected {expected_type.__name__})",
            context=key,
        )
    return value


def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    if (value := d.get(key)) is None:
        return None
    if not isinstance(value, expected_type):
        raise PylockValidationError(
            f"Unexpected type {type(value).__name__} "
            f"(expected {expected_type.__name__})",
            context=key,
        )
    return value


def _get(d, key, default=None):
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


def _get(
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array | None,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    transforms,
    block_indices=None,
    grid_loop_idx=None,
    clock=None,
    increment_clock: bool = True,
    source_info=None,
    input_name=None,
) -> tuple[jax.Array, jax.Array]:
  """Performs a read from the buffer for `allocation_key_as_array` from the given device and thread."""
  device_id_as_int = int(device_id)
  grid_point_coords_as_tuple = (
      tuple(int(x) for x in grid_point_coords)
      if grid_point_coords is not None
      else None
  )
  thread_id_as_int = int(thread_id)
  allocation_key = HostAllocationKey.from_array(allocation_key_as_array)
  del device_id, grid_point_coords, thread_id, allocation_key_as_array

  transforms = _remove_noop_transforms(transforms)
  _validate_transforms(transforms)
  transforms = jax.tree.map(int, transforms)

  if input_name is not None:
    # NOTE: input_name, block_indices, and grid_loop_idx are set only if this
    # function is being called to read a block from a pallas_call input (at the
    # start of one iteration of the kernel body).
    assert block_indices is not None
    block_indices = tuple(int(x) for x in block_indices)
    assert grid_loop_idx is not None
    grid_loop_idx = tuple(int(x) for x in grid_loop_idx)

  shared_memory = _get_shared_memory()

  global_thread_id = shared_memory.get_global_thread_id(
      device_id_as_int, thread_id_as_int
  )

  read_range = interpret_utils.to_range(transforms)
  ret, (shape, dtype), clock_ = shared_memory.get_buffer_content(
      allocation_key,
      read_range,
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

  # Compute the shape of the read value, assuming the read is fully in-bounds.
  # TODO(jburnim): We already know this shape in the Jaxpr where we insert a
  # callback to `get`.  Should we just pass the shape to `get`?
  # TODO(jburnim): Move to a helper function?
  new_full_read_shape: list[int] = []
  assert len(read_range) <= len(shape)
  for dim_size, idx_or_slice in itertools.zip_longest(
      shape, read_range, fillvalue=None
  ):
    assert isinstance(dim_size, int)
    if idx_or_slice is None:
      new_full_read_shape.append(dim_size)
    elif isinstance(idx_or_slice, int):
      continue
    else:
      dim_size = (idx_or_slice.stop - idx_or_slice.start) // idx_or_slice.step
      assert isinstance(dim_size, int)
      new_full_read_shape.append(dim_size)
  full_read_shape = tuple(new_full_read_shape)
  del new_full_read_shape

  if (ret is None) or (full_read_shape != ret.shape):
    ret = _handle_out_of_bounds_read(
        ret,
        full_read_shape,
        shape,
        dtype,
        allocation_key,
        read_range,
        shared_memory,
        source_info,
        input_name,
        block_indices,
        grid_loop_idx,
    )

  if shared_memory.detect_races:
    get_races().check_read(
        device_id_as_int,
        thread_id_as_int,
        clock,
        allocation_key,
        read_range,
        source_info=source_info,
    )
  return token, jnp.array(ret)

