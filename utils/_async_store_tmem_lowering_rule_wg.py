
def _async_store_tmem_lowering_rule_wg(
    ctx: lowering.LoweringRuleContext,
    x_ref: ir.Value,
    value: ir.Value,
    *leaves,
    tree,
):
  assert isinstance(x_ref, ir.Value)
  assert isinstance(x_ref.type, ir.MemRefType)
  assert isinstance(value, ir.Value)
  assert isinstance(value.type, ir.VectorType)
  x_aval = ctx.avals_in[0]
  assert isinstance(x_aval, state_types.AbstractRef)

  transforms = jax.tree.unflatten(tree, leaves)
  transform_avals = tree.unflatten(
      ctx.avals_in[2 : 2 + tree.num_leaves]
  )
  x_tmem, _, transforms = lowering._handle_transforms(
      ctx,
      x_aval,
      x_ref,
      transform_avals,
      transforms,
      handle_transposes=False,
      handle_reshapes=False,
  )
  batch_shape = ()
  if transforms and isinstance(
      transforms[0], gpu_core.ExpandLeadingBatchDimensionsTransform
  ):
    batch_shape = transforms[0].batch_shape
    transforms = transforms[1:]
  if transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for TMEM refs. {transforms=}"
    )
  if batch_shape:
    m, n = ir.VectorType(value.type).shape[-2:]
    for batch_idx in np.ndindex(batch_shape):
      flat_batch_idx = int(np.ravel_multi_index(batch_idx, batch_shape))
      val_slice = vector_dialect.extract(
          value, dynamic_position=[], static_position=batch_idx
      )
      col_start = flat_batch_idx * n
      tmem_slice = mgpu_utils.memref_slice(
          x_tmem, (slice(0, m), slice(col_start, col_start + n))
      )
      mgpu.dialect.async_store_tmem(val_slice, tmem_slice)
  else:
    mgpu.dialect.async_store_tmem(value, x_tmem)
  return ()

