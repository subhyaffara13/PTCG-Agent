
def query_cluster_cancel(cancellation_result: _ods_ir.Value[_ods_ir.MemRefType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return QueryClusterCancelOp(cancellation_result=cancellation_result, results=results, loc=loc, ip=ip).results


def query_cluster_cancel(
    result_ref: _Ref,
    grid_names: Sequence[Hashable]) -> tuple[tuple[jax.Array, ...], jax.Array]:
  """Decodes the result of a ``try_cluster_cancel`` operation.

  It interprets the 16-byte opaque response written to shared memory by a
  completed ``try_cluster_cancel`` call to determine if a new work unit was
  successfully claimed.

  Args:
    result_ref: The SMEM ref containing the query response.
    grid_names: A tuple of grid axis names to query for.

  Returns:
    A tuple containing the decoded response:
      - the grid indices for the requested axis names.
      - A boolean indicating if the cancellation was successful.

  See also:
    :func:`jax.experimental.pallas.mosaic_gpu.try_cluster_cancel`
  """
  if isinstance(result_ref, pallas_core.TransformedRef):
    result_transforms_leaves, result_transforms_tree = jax.tree.flatten(
        result_ref.transforms
    )
    result_ref = result_ref.ref
  else:
    result_transforms_leaves, result_transforms_tree = [], None
  result = query_cluster_cancel_p.bind(
      result_ref,
      *result_transforms_leaves,
      grid_names=grid_names,
      transforms_tree=result_transforms_tree)
  return tuple(result[:-1]), result[-1]


def query_cluster_cancel(
    result_ref,
) -> tuple[ir.Value, ir.Value, ir.Value, ir.Value]:
  """Decodes the response of `try_cluster_cancel`.

  It checks if the cancellation was successful, and if yes, it also extracts
  the CTA ID of the first CTA in the canceled cluster.
  """

  i32 = ir.IntegerType.get_signless(32)
  i1 = ir.IntegerType.get_signless(1)
  struct_ty = llvm.StructType.get_literal([i32, i32, i32, i1])
  desc = llvm.inline_asm(
      struct_ty,
      [memref_ptr(result_ref)],
      """
    {
        .reg .b128 handle;
        ld.shared.b128 handle, [$4];
        clusterlaunchcontrol.query_cancel.is_canceled.pred.b128 $3, handle;
        @$3 clusterlaunchcontrol.query_cancel.get_first_ctaid.v4.b32.b128 {$0, $1, $2, _},  handle;
    }""",
      "=r,=r,=r,=b,r",
  )
  assert isinstance(desc, ir.Value)
  cta_id_x = llvm.extractvalue(i32, desc, [0])
  cta_id_y = llvm.extractvalue(i32, desc, [1])
  cta_id_z = llvm.extractvalue(i32, desc, [2])
  cancelled_launch = llvm.extractvalue(i1, desc, [3])
  return cta_id_x, cta_id_y, cta_id_z, cancelled_launch

