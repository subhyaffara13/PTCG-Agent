
def tcgen05_commit_arrive(barrier: _ods_ir.Value[_ods_ir.MemRefType], *, collective: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TcGen05CommitArriveOp:
  return TcGen05CommitArriveOp(barrier=barrier, collective=collective, loc=loc, ip=ip)


def tcgen05_commit_arrive(barrier: _Ref,
                          collective_axis: str | None = None):
  """Tracks completion of all preceding ``tcgen05_mma`` and ``async_copy_smem_to_tmem`` calls.

  Args:
    barrier: Barrier Ref for synchronizing with the tensor core. Must have
      orders_tensor_core set to True.
    collective_axis: The name of the cluster axis along which the
      operations were performed if it was collective. The cluster axis should
      have a size of exactly 2, and must be on the minormost cluster axis.

  See also:
    - :func:`jax.experimental.pallas.mosaic_gpu.tcgen05_mma`
    - :func:`jax.experimental.pallas.mosaic_gpu.async_copy_smem_to_tmem`
  """
  if isinstance(barrier, pallas_core.TransformedRef):
    barrier_transforms_leaves, barrier_transforms_tree = jax.tree.flatten(
        barrier.transforms
    )
    barrier = barrier.ref
  else:
    barrier_transforms_leaves, barrier_transforms_tree = [], None

  tcgen05_commit_arrive_p.bind(
      barrier, *barrier_transforms_leaves,
      barrier_transforms_tree=barrier_transforms_tree,
      collective_axis=collective_axis)

