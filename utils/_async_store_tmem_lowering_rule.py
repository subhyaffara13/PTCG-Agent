
def _async_store_tmem_lowering_rule(
    ctx: lowering.LoweringRuleContext, x_ref, value, *leaves, tree
):
  assert isinstance(x_ref, tcgen05.TMEMRef)
  x_aval = ctx.avals_in[0]
  assert isinstance(x_aval, state_types.AbstractRef)
  transforms = jax.tree.unflatten(tree, leaves)
  transform_avals = tree.unflatten(
      ctx.avals_in[2 : 2 + tree.num_leaves]
  )
  x_tmem, _, transforms = lowering._handle_transforms(
      ctx, x_aval, x_ref, transform_avals, transforms, handle_transposes=False,
      handle_reshapes=False)
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
    m, n = value.shape[-2:]
    for batch_idx in np.ndindex(batch_shape):
      flat_batch_idx = int(np.ravel_multi_index(batch_idx, batch_shape))
      # TODO(allanrenucci): Add direct support for indexing to FragmentedArray.
      slices = tuple(slice(i, i + 1) for i in batch_idx)
      val_slice = value[slices].reshape((m, n))
      col_start = flat_batch_idx * n
      tmem_slice = x_tmem.slice(slice(0, m), slice(col_start, col_start + n))
      tmem_slice.store(val_slice)
  else:
    x_tmem.store(value)
  return ()

