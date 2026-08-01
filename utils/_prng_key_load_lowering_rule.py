
def _prng_key_load_lowering_rule(ctx: LoweringRuleContext, *args_flat, args_tree) -> KeyScalarBundle:
  """Lowering rule for loading PRNG keys from SMEM.

  PRNG key loads are currently lowered as a list of scalar loads from SMEM,
  rather than a single vector load.
  We store these scalars in a bundle type called KeyScalarBundle, which has
  special case handling for functions that consume the key such as set_seed.
  """
  ref, transforms, _, _ = args_tree.unflatten(args_flat)
  ref_aval, transforms_avals, _, _ = args_tree.unflatten(
      ctx.avals_in
  )
  prev_transforms, idx = _canonicalize_transforms_to_indexer(
      ref_aval, transforms, transforms_avals
  )
  (aval_out,) = ctx.avals_out
  assert isinstance(aval_out.dtype, prng.KeyTy)
  key_shape = aval_out.dtype._impl.key_shape
  ref_block_shape, *_ = ctx.block_shapes
  idx = cast(NDIndexer, idx)
  ref, ref_block_shape = _transform_ref(
      ref, ref_aval, ref_block_shape, prev_transforms
  )

  if len(key_shape) != 2:
    raise NotImplementedError("Seed key_data must be 1D.")
  if key_shape[0] != 1:
    raise NotImplementedError("Leading dimension of seed key_data must be 1.")
  if not all(s == 1 for s in idx.shape):
    raise NotImplementedError("Can only load a single key per load.")
  assert ref_block_shape[-2:] == key_shape, f"{ref_block_shape=} {key_shape=}"

  load_ops = []
  for i in range(key_shape[1]):
    ref_shape = tuple(
        dim for dim in ref_block_shape if dim is not pallas_core.squeezed
    )
    scalar_idx = NDIndexer(
        indices=(*idx.indices, 0, i), shape=ref_shape, int_indexer_shape=()
    )
    starts, _, _, _, _ = _indexer_to_start_size_stride(
        scalar_idx,
        ref_block_shape,
        cast_to_index=True,
    )
    load_ops.append(memref.load(ref, starts))
  return KeyScalarBundle(scalars=load_ops, key_shape=tuple(key_shape))

