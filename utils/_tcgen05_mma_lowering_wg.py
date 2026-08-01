
def _tcgen05_mma_lowering_wg(
    ctx: lowering.LoweringRuleContext,
    acc_ref,
    a_ref,
    b_ref,
    accumulate: bool | ir.Value,
    *barrier_scales_and_transforms_leaves,
    acc_transforms_tree,
    a_transforms_tree,
    b_transforms_tree,
    barrier_transforms_tree,
    a_scale_transforms_tree,
    b_scale_transforms_tree,
    a_sparse_metadata_transforms_tree,
    collective_axis,
    arrive,
    scaled: bool,
    sparse: bool,
):
  (
      acc_aval,
      a_aval,
      b_aval,
      accumulate_aval,
      *_,
  ) = ctx.avals_in
  assert isinstance(acc_aval, state_types.AbstractRef)
  assert isinstance(a_aval, state_types.AbstractRef)
  assert isinstance(b_aval, state_types.AbstractRef)
  del accumulate_aval

  leaves = list(barrier_scales_and_transforms_leaves)
  avals = list(ctx.avals_in[4:])
  if arrive:
    barrier_ref, leaves = leaves[0], leaves[1:]
    barrier_ref_aval, avals = avals[0], avals[1:]
  else:
    barrier_ref = None
    barrier_ref_aval = None

  if scaled:
    # Scales are not supported for WG semantics, but we still need to unpack them
    # if they are present in the leaves/avals to get to the transforms.
    a_scale_ref, b_scale_ref, leaves = leaves[0], leaves[1], leaves[2:]
    a_scale_ref_aval, b_scale_ref_aval, avals = avals[0], avals[1], avals[2:]
  else:
    a_scale_ref = b_scale_ref = a_scale_ref_aval = b_scale_ref_aval = None

  if sparse:
    a_sparse_metadata_ref, leaves = leaves[0], leaves[1:]
    a_sparse_metadata_ref_aval, avals = avals[0], avals[1:]
  else:
    a_sparse_metadata_ref = a_sparse_metadata_ref_aval = None

  transforms_trees = (
      acc_transforms_tree,
      a_transforms_tree,
      b_transforms_tree,
      barrier_transforms_tree,
      a_scale_transforms_tree,
      b_scale_transforms_tree,
      a_sparse_metadata_transforms_tree,
  )
  ns = [getattr(tree, "num_leaves", 0) for tree in transforms_trees]
  transforms_leaves_lists = util.split_list_checked(leaves, ns)
  transforms_avals_lists = util.split_list_checked(avals, ns)

  (
      acc_transforms_leaves,
      a_transforms_leaves,
      b_transforms_leaves,
      barrier_transforms_leaves,
      a_scale_transforms_leaves,
      b_scale_transforms_leaves,
      a_sparse_metadata_transforms_leaves,
  ) = transforms_leaves_lists

  (
      acc_transforms_leaves_avals,
      a_transforms_leaves_avals,
      b_transforms_leaves_avals,
      _,
      a_scale_transforms_leaves_avals,
      b_scale_transforms_leaves_avals,
      a_sparse_metadata_transforms_leaves_avals,
  ) = transforms_avals_lists

  def handle_transforms_and_get_ref(tree, leaves, leaves_avals, ref, ref_aval, handle_transposes=True):
    if tree is None:
      return ref
    transforms = tree.unflatten(leaves)
    transform_avals = tree.unflatten(leaves_avals)
    ref, _, transforms = lowering._handle_transforms(
        ctx, ref_aval, ref, transform_avals, transforms, handle_transposes=handle_transposes
    )
    if transforms:
      raise NotImplementedError(
          f"Unsupported transforms for {ref}. Transforms {transforms}."
      )
    return ref

  acc_ref = handle_transforms_and_get_ref(
      acc_transforms_tree,
      acc_transforms_leaves,
      acc_transforms_leaves_avals,
      acc_ref,
      acc_aval,
      handle_transposes=False,
  )

  a_ref = handle_transforms_and_get_ref(
      a_transforms_tree,
      a_transforms_leaves,
      a_transforms_leaves_avals,
      a_ref,
      a_aval,
      handle_transposes=a_aval.memory_space == gpu_core.SMEM
  )

  b_ref = handle_transforms_and_get_ref(
      b_transforms_tree,
      b_transforms_leaves,
      b_transforms_leaves_avals,
      b_ref,
      b_aval,
  )

  a_sparse_metadata_ref = handle_transforms_and_get_ref(
      a_sparse_metadata_transforms_tree,
      a_sparse_metadata_transforms_leaves,
      a_sparse_metadata_transforms_leaves_avals,
      a_sparse_metadata_ref,
      a_sparse_metadata_ref_aval,
  )

  if barrier_transforms_tree is not None and barrier_ref is not None:
    barrier_transforms = barrier_transforms_tree.unflatten(
        barrier_transforms_leaves
    )
    base_index = _get_barrier_base_index(barrier_ref_aval, barrier_transforms)
    if base_index is not None:
      barrier_ref = barrier_ref[base_index]

  a_scale_ref = handle_transforms_and_get_ref(
      a_scale_transforms_tree,
      a_scale_transforms_leaves,
      a_scale_transforms_leaves_avals,
      a_scale_ref,
      a_scale_ref_aval,
  )

  b_scale_ref = handle_transforms_and_get_ref(
      b_scale_transforms_tree,
      b_scale_transforms_leaves,
      b_scale_transforms_leaves_avals,
      b_scale_ref,
      b_scale_ref_aval,
  )

  predicate_ctx: contextlib.AbstractContextManager[None]
  if collective_axis is not None:
    predicate_ctx = mgpu.when(_collective_mma_predicate(ctx, collective_axis))
    collective = True
  else:
    predicate_ctx = contextlib.nullcontext()
    collective = False

  if isinstance(accumulate, bool):
    i1 = ir.IntegerType.get_signless(1)
    accumulate = arith_dialect.constant(i1, accumulate)

  with predicate_ctx:
    mgpu.dialect.tcgen05_mma(
        acc_ref,
        a_ref,
        b_ref,
        accumulate=accumulate,
        collective=collective,
        a_scale=a_scale_ref,
        b_scale=b_scale_ref,
        a_sparse_metadata=a_sparse_metadata_ref,
    )
    if arrive:
      assert isinstance(barrier_ref, mgpu.DialectBarrierRef)
      mgpu.dialect.tcgen05_commit_arrive(
          barrier_ref.as_barrier_memref(), collective=collective
      )
  return []

