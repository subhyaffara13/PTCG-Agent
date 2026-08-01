
def _inline_mgpu_flat_transformed_args(
    ctx: lowering.LoweringRuleContext,
    flat_args_and_transforms,
    flat_arg_types,
    pytree_args,
    pytree_ref_transforms,
  ) -> Sequence[ir.Value | mgpu.FragmentedArray]:
  flat_args = flat_args_and_transforms[:pytree_args.num_leaves]
  flat_arg_avals = ctx.avals_in[:pytree_args.num_leaves]
  ref_transforms = pytree_ref_transforms.unflatten(flat_args_and_transforms[pytree_args.num_leaves:])
  ref_transform_avals = pytree_ref_transforms.unflatten(ctx.avals_in[pytree_args.num_leaves:])
  is_wg_semantics = (
      ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup
  )
  is_warp_semantics = (
      ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp
  )

  if is_wg_semantics:
    flat_args = [
        lowering._ensure_ir_value(a, aval.dtype) if not isinstance(t, RefType) else a
        for a, aval, t in zip(flat_args, flat_arg_avals, flat_arg_types)
    ]
  else:
    flat_args = [
        lowering._ensure_fa(a, aval.dtype) if not isinstance(t, RefType) else a
        for a, aval, t in zip(flat_args, flat_arg_avals, flat_arg_types)
    ]

  for a, aval, t in zip(flat_args, flat_arg_avals, flat_arg_types):
    if not is_wg_semantics:
      _type_check_mgpu_lane_semantics(a, t)
    if is_warp_semantics and not isinstance(t, RefType):
      if not isinstance(aval, jax_core.ShapedArray) or aval.shape:
        raise ValueError(
            "inline_mgpu in a single-warp context only supports scalar"
            f" arrays (and Refs). Got {aval}."
        )

  flat_transformed : list[ir.Value | mgpu.FragmentedArray] = []
  for a, aval, t, transforms, transform_avals in zip(
      flat_args,
      flat_arg_avals,
      flat_arg_types,
      ref_transforms,
      ref_transform_avals,
      strict=True,
  ):
    if not isinstance(t, RefType):
      flat_transformed.append(a)
      assert transforms is None
      continue
    assert isinstance(aval, state.AbstractRef)
    assert isinstance(a, ir.Value)
    a, aval, user_transforms = lowering._handle_transforms(
        ctx,
        aval,
        a,
        transform_avals,
        transforms,
        handle_transposes=is_wg_semantics,
    )

    if is_wg_semantics:
      if user_transforms:
        raise NotImplementedError(
            "Not all transforms could be handled. Remaining transforms:"
            f" {user_transforms}."
        )
    else:
      # Transforms that do not originate from a MemoryRefTransform are
      # applied implicitly (eg by emit-pipeline) and therefore we do not
      # expect the user to pass them to the type. The transforms not
      # passed by the user here will be discharged.
      ty_transforms = tuple(pallas_core.undo_transforms(aval, t.transforms))
      if ty_transforms != tuple(user_transforms):
        raise ValueError(
            f"Transform mismatch: got {user_transforms}, expected"
            f" {ty_transforms}"
        )
    flat_transformed.append(a)

  return flat_transformed

