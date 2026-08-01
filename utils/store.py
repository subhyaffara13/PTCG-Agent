
def store(ptr: _ods_ir.Value, value: _ods_ir.Value, *, mask: _Optional[_ods_ir.Value] = None, cache: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, evict: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, ignore_cta: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StoreOp:
  return StoreOp(ptr=ptr, value=value, mask=mask, cache=cache, evict=evict, ignore_cta=ignore_cta, loc=loc, ip=ip)


def store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], sublane_mask: _Union[_Sequence[bool], _ods_ir.DenseBoolArrayAttr], *, mask: _Optional[_ods_ir.Value] = None, sublane_stride: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, add: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StoreOp:
  return StoreOp(valueToStore=value_to_store, base=base, indices=indices, sublane_mask=sublane_mask, mask=mask, sublane_stride=sublane_stride, add=add, loc=loc, ip=ip)


def store(value: _ods_ir.Value, addr: _ods_ir.Value, *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, volatile_: _Optional[bool] = None, nontemporal: _Optional[bool] = None, invariant_group: _Optional[bool] = None, ordering: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, syncscope: _Optional[_Union[str, _ods_ir.StringAttr]] = None, access_groups: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, alias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, noalias_scopes: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, tbaa: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StoreOp:
  return StoreOp(value=value, addr=addr, alignment=alignment, volatile_=volatile_, nontemporal=nontemporal, invariantGroup=invariant_group, ordering=ordering, syncscope=syncscope, access_groups=access_groups, alias_scopes=alias_scopes, noalias_scopes=noalias_scopes, tbaa=tbaa, loc=loc, ip=ip)


def store(value: _ods_ir.Value, memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, nontemporal: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StoreOp:
  return StoreOp(value=value, memref=memref, indices=indices, nontemporal=nontemporal, alignment=alignment, loc=loc, ip=ip)


def store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, nontemporal: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StoreOp:
  return StoreOp(valueToStore=value_to_store, base=base, indices=indices, nontemporal=nontemporal, alignment=alignment, loc=loc, ip=ip)


def store(x_ref_or_view, idx, val, *, mask=None, eviction_policy=None) -> None:
  """Stores a value at the given index.

  See :func:`~jax.experimental.pallas.load` for the meaning of the arguments.
  """
  _ = swap(x_ref_or_view, idx, val, mask=mask, eviction_policy=eviction_policy,
           _function_name="store")


def store(ref: Ref, val: jax.Array, *, mask: jax.Array | None = None) -> None:
  """Stores a value to the given ref.

  If ``mask`` is not specified, this function has the same semantics as
  ``ref[idx] = val`` in JAX.

  Args:
    ref: The ref to store to.
    val: The value to store.
    mask: An optional boolean mask specifying which indices to store.
  """
  return primitives.store(ref, None, val, mask=mask)


def store(
    ref: Ref,
    val: jax.Array,
    *,
    mask: jax.Array | None = None,
    eviction_policy: str | None = None,
) -> None:
  """Stores a value to the given ref.

  See :func:`~jax.experimental.pallas.load` for the meaning of the arguments.
  """
  return pallas_primitives.store(
      ref,
      None,
      val,
      mask=mask,
      eviction_policy=eviction_policy,
  )


def store(
    token,
    device_id,
    local_core_id,
    memory_space,
    buffer_id,
    transforms,
    val,
    block_indices=None,
    grid_loop_idx=None,
    *,
    src_device_id=None,
    src_local_core_id=None,
    clock=None,
    source_info=None,
    output_name=None,
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
  src_device_id = _to_int(src_device_id)
  src_local_core_id = _to_int(src_local_core_id)
  if output_name is not None:
    # NOTE: output_name, block_indices, and grid_loop_idx are set only if this
    # function is being called to store a block into a pallas_call output (at
    # the end of one iteration of the kernel body).
    assert block_indices is not None
    block_indices = tuple(int(x) for x in block_indices)
    assert grid_loop_idx is not None
    grid_loop_idx = tuple(int(x) for x in tuple(grid_loop_idx))

  shared_memory = _get_shared_memory()

  local_core_id_for_buffer = _local_core_id_or_zero_if_hbm(
      local_core_id, memory_space
  )
  global_core_id = shared_memory.get_global_core_id(device_id, local_core_id)

  key = (memory_space, buffer_id, device_id, local_core_id_for_buffer)
  write_range = interpret_utils.to_range(transforms)
  in_bounds, (shape, _), clock_ = shared_memory.store_buffer_content(
      key,
      write_range,
      val,
      global_core_id,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  clock = clock if clock is not None else clock_

  if not in_bounds:
    if output_name is None:
      raise ValueError(
          'Out-of-bounds write of'
          f' ({device_id} {local_core_id} {memory_space} {buffer_id}):'
          f' writing [{write_range}] but buffer has shape {shape} .'
      )
    else:
      # Different error message when we are copying a kernel buffer to a
      # block of an output (just after a kernel invocation).
      raise IndexError(
          f'Out-of-bounds block index {block_indices} for'
          f' output "{output_name}" in iteration {grid_loop_idx}'
          f' on device {device_id} (core {local_core_id}):'
          f' reading [{write_range}] but output has shape {shape}.'
      )

  if shared_memory.detect_races:
    if src_device_id is None:
      src_device_id = device_id
    if src_local_core_id is None:
      src_local_core_id = local_core_id
    assert races is not None
    races.check_write(
        src_device_id,
        src_local_core_id,
        clock,
        (memory_space, buffer_id, device_id, local_core_id_for_buffer),
        write_range,
        source_info=source_info,
    )
  return token

