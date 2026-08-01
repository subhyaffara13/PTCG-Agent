
def try_cluster_cancel(cancellation_result: _ods_ir.Value[_ods_ir.MemRefType], barrier: _ods_ir.Value[_ods_ir.MemRefType], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TryClusterCancelOp:
  return TryClusterCancelOp(cancellation_result=cancellation_result, barrier=barrier, predicate=predicate, loc=loc, ip=ip)


def try_cluster_cancel(result_ref: _Ref, barrier: _Ref) -> None:
  """Initiates an async request to claim a new work unit from the grid.

  It allows an SM to dynamically acquire work by atomically canceling the launch
  of a pending cluster from the grid and claiming its CTA ID as the next unit
  of work.

  Note that this operation must be called collectively by all Pallas threads.

  Args:
    result_ref: An SMEM ref where the 16-byte result will be stored.
    barrier: A barrier used to coordinate the completion of the query.

  See also:
    :func:`jax.experimental.pallas.mosaic_gpu.query_cluster_cancel`
  """
  if isinstance(result_ref, pallas_core.TransformedRef):
    result_transforms_leaves, result_transforms_tree = jax.tree.flatten(
        result_ref.transforms
    )
    result_ref = result_ref.ref
  else:
    result_transforms_leaves, result_transforms_tree = [], None

  if isinstance(barrier, pallas_core.TransformedRef):
    barrier_transforms_leaves, barrier_transforms_tree = jax.tree.flatten(
        barrier.transforms
    )
    barrier = barrier.ref
  else:
    barrier_transforms_leaves, barrier_transforms_tree = [], None

  try_cluster_cancel_p.bind(
      result_ref,
      barrier,
      *result_transforms_leaves,
      *barrier_transforms_leaves,
      result_transforms_tree=result_transforms_tree,
      barrier_transforms_tree=barrier_transforms_tree,
  )


def try_cluster_cancel(
    result_ref,
    barrier: BarrierRef,
    predicate: ir.Value | None = None,
):
  """Atomically cancels a pending cluster launch.

  The response is stored in a opaque 128-bit value containing the CTA id of the
  first CTA in the canceled cluster.
  """
  if predicate is None:
    predicate = single_thread_predicate(ThreadSubset.BLOCK)
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [memref_ptr(result_ref), barrier.get_ptr(), predicate],
      "@$2 clusterlaunchcontrol.try_cancel.async.shared::cta.mbarrier::complete_tx::bytes.multicast::cluster::all.b128"
      " [$0], [$1];",
      "r,r,b",
      has_side_effects=True,
  )

