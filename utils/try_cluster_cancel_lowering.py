import math


def try_cluster_cancel_lowering(
    ctx: lowering.LoweringRuleContext,
    result_ref,
    barrier,
    *transforms_leaves,
    result_transforms_tree,
    barrier_transforms_tree,
):
  i1 = ir.IntegerType.get_signless(1)
  i32 = ir.IntegerType.get_signless(32)

  if result_transforms_tree is not None:
    res_transforms_leaves, barrier_transforms_leaves = util.split_list(
      transforms_leaves, [result_transforms_tree.num_leaves])
    res_transforms = result_transforms_tree.unflatten(res_transforms_leaves)
    res_transform_avals = result_transforms_tree.unflatten(
        ctx.avals_in[2 : 2 + result_transforms_tree.num_leaves]
    )
    result_aval = ctx.avals_in[0]
    assert isinstance(result_aval, state_types.AbstractRef)
    result_ref, _, res_transforms = lowering._handle_transforms(
        ctx, result_aval, result_ref, res_transform_avals, res_transforms)
    if res_transforms:
      raise NotImplementedError(
          f"Unimplemented transforms for result ref: {res_transforms}"
      )
  else:
    barrier_transforms_leaves = transforms_leaves

  if barrier_transforms_tree is not None:
    base_index = _get_barrier_base_index(
        ctx.avals_in[1],
        barrier_transforms_tree.unflatten(barrier_transforms_leaves),
    )
    if base_index is not None:
      barrier = barrier[base_index]

  result_ty = ir.MemRefType(result_ref.type)
  bits = math.prod(result_ty.shape) * mgpu.bitwidth(result_ty.element_type)
  if bits != 128:
    raise TypeError(
        f"Try cluster cancel response must be 128 bits, but is {bits} bits."
    )

  is_first_wg = arith_dialect.cmpi(
      arith_dialect.CmpIPredicate.eq, mgpu.warpgroup_idx(), mgpu.c(0, i32)
  )

  is_first_cta = mgpu.c(1, i1)
  for dim in gpu_dialect.Dimension:
    is_first_cta = arith_dialect.andi(
        is_first_cta,
        arith_dialect.cmpi(
            arith_dialect.CmpIPredicate.eq,
            mgpu.utils.cluster_idx(dim),
            mgpu.c(0, ir.IndexType.get()),
        ),
    )

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:

    # TODO(b/415721295): Check whether this is slower than doing
    # arrive_expect_tx(select(is_first_wg, 16, 0)) and if so then implement
    # support for ir.Value in arrive_expect_tx in the MGPU dialect (right now
    # the tx_bytes is an attribute, not an operand).
    with mgpu.utils.when(is_first_wg):
      barrier.arrive_expect_tx(16)
    with mgpu.utils.when(arith_dialect.xori(is_first_wg, mgpu.c(1, i1))):
      barrier.arrive()
    mgpu.dialect.try_cluster_cancel(
        result_ref,
        barrier.as_barrier_memref(),
        predicate=arith_dialect.andi(is_first_cta, is_first_wg))
  else:
    assert ctx.module_ctx.single_lane_predicate is not None
    is_leader_thread = arith_dialect.andi(
        ctx.module_ctx.single_lane_predicate, is_first_wg
    )
    bytes = arith_dialect.select(is_leader_thread, mgpu.c(16, i32), mgpu.c(0, i32))
    barrier.arrive_expect_tx(bytes)
    mgpu.try_cluster_cancel(
        result_ref,
        barrier,
        predicate=arith_dialect.andi(is_leader_thread, is_first_cta),
    )

  return []

