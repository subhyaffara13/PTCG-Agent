from typing import Any, Callable

def _inline_mgpu_lowering_rule(
    ctx: lowering.LoweringRuleContext,
    *flat_args_and_transforms,
    mgpu_fn: Callable[..., Any],
    flat_arg_types,
    flat_ret_ty,
    pytree_args,
    pytree_ref_transforms,
    pytree_ret_ty,
):
  is_warp_semantics = (
      ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp
  )
  if is_warp_semantics:
    for r in flat_ret_ty:
      if isinstance(r, ShapeDtypeStruct) and r.shape:
        raise ValueError(
            "inline_mgpu in a single-warp context only supports scalar return"
            f" types. Got shape={r.shape}."
        )

  flat_transformed = _inline_mgpu_flat_transformed_args(
      ctx,
      flat_args_and_transforms,
      flat_arg_types,
      pytree_args,
      pytree_ref_transforms,
  )
  args = jax.tree.unflatten(pytree_args, flat_transformed)
  ret = mgpu_fn(ctx.launch_ctx, *args)
  ret_leaves, ret_tree = jax.tree.flatten(
      ret, lambda x: isinstance(x, mgpu.FragmentedArray)
  )

  if ret_tree != pytree_ret_ty:
    return_type = jax.tree.unflatten(pytree_ret_ty, flat_ret_ty)
    raise ValueError(
        f"inline_mgpu_p return type tree mismatch: {ret} != {return_type}"
    )

  for ty, r in zip(flat_ret_ty, ret_leaves):
    _type_check_mgpu_lane_semantics(r, ty)

  return ret_leaves

