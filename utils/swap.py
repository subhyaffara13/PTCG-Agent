
def swap(x_ref_or_view, idx, val, *, mask=None, eviction_policy=None,
         _function_name="swap") -> jax_typing.Array:
  """Swaps the value at the given index and returns the old value.

  See :func:`~jax.experimental.pallas.load` for the meaning of the arguments.

  Returns:
    The value stored in the ref prior to the swap.
  """
  x_ref, transforms = sp.get_ref_and_transforms(
      x_ref_or_view, idx, _function_name
  )
  args_flat, args_tree = tree_util.tree_flatten((x_ref, transforms, val, mask))
  return swap_p.bind(
      *args_flat, args_tree=args_tree, eviction_policy=eviction_policy
  )


def swap(
    token,
    device_id,
    local_core_id,
    memory_space,
    buffer_id,
    transforms,
    val,
    mask,
    *,
    source_info=None,
):
  device_id = int(device_id)
  local_core_id = int(local_core_id)
  memory_space = TPU_MEMORY_SPACE_NAMES[int(memory_space)]
  buffer_id = int(buffer_id)
  try:
    transforms = jax.tree.map(int, transforms)
  except:
    raise ValueError('Advanced indexers are not supported on TPU')
  val = np.array(val)
  mask = np.array(mask) if mask is not None else None
  if mask is not None:
    assert mask.shape == val.shape

  shared_memory = _get_shared_memory()

  local_core_id_for_buffer = _local_core_id_or_zero_if_hbm(
      local_core_id, memory_space
  )
  global_core_id = shared_memory.get_global_core_id(device_id, local_core_id)

  key = (memory_space, buffer_id, device_id, local_core_id_for_buffer)
  read_write_range = interpret_utils.to_range(transforms)
  ret, (shape, _), clock = shared_memory.swap_buffer_content(
      key,
      read_write_range,
      val,
      mask,
      global_core_id,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )

  if ret is None:
    if mask is None:
      raise ValueError(
          'Out-of-bounds swap of'
          f' ({device_id} {local_core_id} {memory_space} {buffer_id}):'
          f' swapping [{read_write_range}] but buffer has shape'
          f' {shape} .'
      )
    else:
      # TODO(jburnim): Include indices of out-of-bounds locations where mask
      # is True.
      raise ValueError(
          'Out-of-bounds masked swap of'
          f' ({device_id} {local_core_id} {memory_space} {buffer_id}): swapping'
          f' [{read_write_range}] but buffer has shape {shape} . '
      )

  if shared_memory.detect_races:
    assert races is not None
    races.check_write(
        device_id,
        local_core_id,
        clock,
        (memory_space, buffer_id, device_id, local_core_id_for_buffer),
        read_write_range,
        source_info=source_info,
    )
  return token, ret

