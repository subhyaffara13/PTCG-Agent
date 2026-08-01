
def copy_smem_to_gmem(
    src: _Ref,
    dst: _Ref,
    predicate: jax.Array | None = None,
    *,
    commit_group: bool = True,
    reduction_op: mgpu.TMAReductionOp | None = None,
) -> None:
  """Asynchronously copies a SMEM reference to a GMEM reference.

  Args:
    src: The SMEM reference to copy from.
    dst: The GMEM reference to copy to.
    predicate: A boolean indicating whether the copy should be performed. If
      ``None``, the copy is always performed.
    commit_group: If ``True``, this and any previously uncommitted copies are
      committed to a group and can be awaited jointly via
      :func:`jax.experimental.pallas.mosaic_gpu.wait_smem_to_gmem`.
    reduction_op: If set, perform the specified reduction operation when storing
      to GMEM. For example, using ``"add"`` is conceptually equivalent to
      doing ``src += dst``.

  See also:
    :func:`jax.experimental.pallas.mosaic_gpu.wait_smem_to_gmem`
    :func:`jax.experimental.pallas.mosaic_gpu.commit_smem`
  """
  src, src_transforms = state_primitives.get_ref_and_transforms(
      src, None, "copy_smem_to_gmem"
  )
  dst, dst_transforms = state_primitives.get_ref_and_transforms(
      dst, None, "copy_smem_to_gmem"
  )
  flat_src_transforms, src_transforms_treedef = tree_util.tree_flatten(
      src_transforms
  )
  flat_dst_transforms, dst_transforms_treedef = tree_util.tree_flatten(
      dst_transforms
  )
  copy_smem_to_gmem_p.bind(
      src,
      dst,
      *flat_src_transforms,
      *flat_dst_transforms,
      *[] if predicate is None else [predicate],
      src_transforms_treedef=src_transforms_treedef,
      dst_transforms_treedef=dst_transforms_treedef,
      has_user_predicate=predicate is not None,
      commit_group=commit_group,
      reduction_op=reduction_op,
  )
  return None


def copy_smem_to_gmem(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    src_allocation_key_as_array: jax.Array,
    src_transforms: tuple[Any, ...],
    dst_allocation_key_as_array: jax.Array,
    dst_transforms: tuple[Any, ...],
    predicate: jax.Array | None,
    source_info: source_info_util.SourceInfo,
    commit_group: bool,
    reduction_op: mgpu.TMAReductionOp,
):
  # TODO(jburnim): Make the copy async, and implement commit_group.
  # TODO(jburnim): Vector clocks and race detection.
  del commit_group
  device_id: int = int(device_id)  # pyrefly: ignore[redefinition]
  grid_point_coords: tuple[int, ...] = jax.tree.map(int, grid_point_coords)  # pyrefly: ignore[redefinition]
  thread_id: int = int(thread_id)  # pyrefly: ignore[redefinition]
  src_allocation_key = HostAllocationKey.from_array(src_allocation_key_as_array)
  src_transforms = jax.tree.map(int, _remove_noop_transforms(src_transforms))  # pyrefly: ignore[redefinition]
  dst_allocation_key = HostAllocationKey.from_array(dst_allocation_key_as_array)
  dst_transforms = jax.tree.map(int, _remove_noop_transforms(dst_transforms))  # pyrefly: ignore[redefinition]

  if predicate is not None:
    raise NotImplementedError("predicate not supported")
  if reduction_op is not None:
    raise NotImplementedError("reduction_op not supported")

  shared_memory = _get_shared_memory()
  global_thread_id = shared_memory.get_global_thread_id(device_id, thread_id)

  logging_info = interpret_utils.GPULoggingInfo(
      device_id=device_id,
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      source_info=source_info,
  )

  val, _, _ = shared_memory.get_buffer_content(
      src_allocation_key, interpret_utils.to_range(src_transforms),
      global_thread_id, logging_info=logging_info)
  assert val is not None
  shared_memory.store_buffer_content(
      dst_allocation_key, interpret_utils.to_range(dst_transforms),
      val,
      global_thread_id, logging_info=logging_info)

  return token

