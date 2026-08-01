
def _jaxpr_call_lowering_rule(
    ctx: LoweringRuleContext,
    *flat_args,
    jaxpr: jax_core.Jaxpr,
    ref_treedefs,
    program_ids_treedef,
):
  args = []
  flat_refs, flat_program_ids = util.split_list(
      flat_args, [sum(treedef.num_leaves for treedef in ref_treedefs)]
  )
  flat_ref_avals, flat_program_ids_avals = util.split_list(
      ctx.avals_in, [sum(treedef.num_leaves for treedef in ref_treedefs)]
  )
  del flat_program_ids_avals  # Unused.
  flat_refs = util.split_list(
      flat_refs,
      [treedef.num_leaves for treedef in ref_treedefs[: len(ref_treedefs) - 1]],
  )
  flat_ref_avals = util.split_list(
      flat_ref_avals,
      [treedef.num_leaves for treedef in ref_treedefs[: len(ref_treedefs) - 1]],
  )
  for treedef, flat_ref, ref_aval in zip(
      ref_treedefs, flat_refs, flat_ref_avals
  ):
    ref = treedef.unflatten(flat_ref)
    ref_aval = treedef.unflatten(ref_aval)
    if isinstance(ref, tuple):
      ref, transforms = ref
      ref_aval, transform_avals = ref_aval
      # We ignore other transforms here, because they are already embedded
      # in the jaxpr.
      assert isinstance(ref_aval, state_types.AbstractRef)
      ref, ref_aval, _ = _handle_transforms(
          ctx, ref_aval, ref, transform_avals, transforms,
          handle_reshapes=False, handle_transposes=False
      )
      if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
        # In warpgroup semantics, we must reapply the transforms that were on
        # the `BlockSpec` here, as the below expects the transformed value to be
        # fed in.
        spec_transforms = tuple(
            t for t in transforms
            if isinstance(t, (gpu_core.UntilingTransform, gpu_core.UnswizzleRef))
        )
        if spec_transforms != transforms[:len(spec_transforms)]:
          raise NotImplementedError(
              "Encountered non-leading UntilingTransform or UnswizzleRef "
              f"transforms: {transforms}"
          )
        for t in pallas_core.undo_transforms(ref_aval, spec_transforms):
          ref_aval = cast(state_types.AbstractRef, t.transform_type(ref_aval))
        ref = _reinterpret_cast(ref, ref_aval)
    args.append(ref)
  program_ids = program_ids_treedef.unflatten(flat_program_ids)
  for axis, pid in enumerate(program_ids):
    if pid is not None:
      continue
    program_ids[axis] = _program_id(
        axis, ctx.module_ctx.squashed_dims, len(program_ids)
    )
  new_module_ctx = dataclasses.replace(ctx.module_ctx, program_ids=program_ids)
  return lower_jaxpr_to_mosaic_gpu(
      new_module_ctx, ctx.launch_ctx, jaxpr, args
  )

