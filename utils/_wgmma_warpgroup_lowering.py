
def _wgmma_warpgroup_lowering(
    ctx: lowering.LoweringRuleContext,
    acc,
    a,
    b,
    *transforms_leaves,
    acc_transforms_tree,
    a_transforms_tree,
    b_transforms_tree,
):
  transform_treedefs = [
      acc_transforms_tree, a_transforms_tree, b_transforms_tree
  ]
  transform_leaves = util.split_list(
      transforms_leaves, [getattr(tree, "num_leaves", 0) for tree in transform_treedefs]
  )
  acc_transforms, a_transforms, b_transforms = (
      None if treedef is None else treedef.unflatten(leaves)
      for treedef, leaves in zip(transform_treedefs, transform_leaves)
  )

  if acc_transforms is not None:
    if not all(isinstance(t, indexing.NDIndexer) for t in acc_transforms):
      raise ValueError("WGMMA accumulator only supports indexing transforms")
    acc_indexer = lowering.merge_indexers(acc_transforms)
    if acc_indexer.int_indexer_shape:
      raise NotImplementedError("int_indexer_shape non-empty")
    acc_indices = lowering._ndindexer_indices(acc_indexer)
  else:
    acc_indices = ()

  transform_avals_list = util.split_list(
      ctx.avals_in[3:], [getattr(tree, "num_leaves", 0) for tree in transform_treedefs]
  )

  if a_transforms is not None:
    a_aval = ctx.avals_in[1]
    assert isinstance(a_aval, state_types.AbstractRef)
    a_transform_avals = a_transforms_tree.unflatten(transform_avals_list[1])
    a, _, a_transforms = lowering._handle_transforms(
        ctx, a_aval, a, a_transform_avals, a_transforms
    )
    if a_transforms:
      raise ValueError(
          f"WGMMA lhs has unsupported transforms: {a_transforms}."
      )

  if b_transforms is not None:
    b_aval = ctx.avals_in[2]
    assert isinstance(b_aval, state_types.AbstractRef)
    b_transform_avals = b_transforms_tree.unflatten(transform_avals_list[2])
    b, _, b_transforms = lowering._handle_transforms(
        ctx, b_aval, b, b_transform_avals, b_transforms
    )
    if b_transforms:
      raise ValueError(
          f"WGMMA rhs has unsupported transforms: {b_transforms}."
      )

  offsets = []
  strides = []
  sizes = []
  for s in acc_indices:
    if not isinstance(s, slice):
      raise NotImplementedError("Only static slices are supported")
    if s.start is None or s.stop is None:
      raise NotImplementedError("Static slices must have start and stop")
    if s.step is not None and s.step != 1:
      raise NotImplementedError("Static slices must have step 1")
    offsets.append(s.start)
    sizes.append(s.stop - s.start)
    strides.append(s.step or 1)

  if acc_indices:
    acc_type = ir.VectorType.get(sizes, ir.VectorType(acc.type).element_type)
    acc_in = vector_dialect.extract_strided_slice(
        acc_type,
        source=acc,
        offsets=offsets,
        sizes=sizes,
        strides=strides,
    )
  else:
    acc_in = acc

  new_acc = mgpu.dialect.wgmma(acc_in, a, b)

  if acc_indices:
    assert offsets and strides
    new_acc = vector_dialect.insert_strided_slice(
        new_acc, acc, offsets, strides
    )

  nvvm_dialect.wgmma_commit_group_sync_aligned()
  return new_acc

