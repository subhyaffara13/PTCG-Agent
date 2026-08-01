
def copy_gmem_to_smem(
    src: _Ref,
    dst: _Ref,
    barrier: _Ref,
    *,
    collective_axes: str | tuple[str, ...] | None = None,
    leader_tracked: CopyPartition | None = None,
    oob_mode: OOBFillMode = OOBFillMode.ZEROS,
) -> None:
  """Asynchronously copies a GMEM reference to a SMEM reference.

  If collective_axes is specified, this performs a multicast copy where
  all CUDA blocks that share the same index along the collective axis
  receive a copy of the same block of data loaded from `dst` to `src`.

  If both ``collective_axes`` and ``leader_tracked`` are specified as
  ``CopyPartition.PARTITIONED(axis)``, this will perform a partitioned
  collective copy where each block in the cluster will receive a tile of
  ``transfer_size // cluster_size`` data from the ``src`` Ref.
  For example, if ``src`` has a shape of (256, 256) and a partitioned
  copy is performed along axis 0 with cluster size 2, then the first block
  will receive ``src[0:128, :]`` and the second will receive
  ``src[128:256, :]``.

  If both ``collective_axes`` and ``leader_tracked`` are specified as
  ``CopyPartition.REPLICATED``, this will perform a replicated copy where
  all blocks load the same data but only the first block in the collective
  tracks progress via barrier arrivals.


  NOTE: Only the first block in the cluster will arrive on the barrier,
  and an additional cluster barrier is necessary to ensure that all blocks in
  the cluster have finished the copy.

  Args:
    src: The source Ref. Must be in GMEM.
    dst: The destination Ref. Must be in SMEM.
    barrier: The barrier to use for tracking completion of the copy.
    collective_axes: The collective axes to use for the copy.
    leader_tracked: If specified, only the leader block in the cluster will
     observe the completion of the copy. If ``CopyPartition.PARTITIONED(axis)``,
     performs a partitioned collective copy along the given axis. If
     ``CopyPartition.REPLICATED``, all blocks load the same data.
    oob_mode: The optional out-of-bounds fill mode. Can be ``OOBFillMode.UNDEFINED``,
     ``OOBFillMode.PROMISE_IN_BOUNDS`` or ``OOBFillMode.ZEROS``.

  See also:
    :func:`jax.experimental.pallas.mosaic_gpu.barrier_arrive`
    :func:`jax.experimental.pallas.mosaic_gpu.barrier_wait`
  """
  src, src_transforms = state_primitives.get_ref_and_transforms(
      src, None, "copy_gmem_to_smem"
  )
  dst, dst_transforms = state_primitives.get_ref_and_transforms(
      dst, None, "copy_gmem_to_smem"
  )
  flat_src_transforms, src_transforms_treedef = tree_util.tree_flatten(
      src_transforms
  )
  flat_dst_transforms, dst_transforms_treedef = tree_util.tree_flatten(
      dst_transforms
  )
  barrier, barrier_transforms = state_primitives.get_ref_and_transforms(
      barrier, None, "copy_gmem_to_smem"
  )
  flat_barrier_transforms, barrier_transforms_treedef = tree_util.tree_flatten(
      barrier_transforms
  )
  if isinstance(collective_axes, str):
    collective_axes = (collective_axes,)
  if leader_tracked is not None and collective_axes is None:
    raise ValueError(
        "`collective_axes` must be specified when `leader_tracked` is set"
    )
  copy_gmem_to_smem_p.bind(
      src,
      dst,
      barrier,
      *flat_src_transforms,
      *flat_dst_transforms,
      *flat_barrier_transforms,
      src_transforms_treedef=src_transforms_treedef,
      dst_transforms_treedef=dst_transforms_treedef,
      barrier_transforms_treedef=barrier_transforms_treedef,
      collective_axes=collective_axes,
      leader_tracked=leader_tracked,
      oob_mode=oob_mode,
  )
  return None

