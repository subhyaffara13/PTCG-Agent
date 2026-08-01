
def _copy_smem_to_gmem_pp_eqn(
    eqn: jax_core.JaxprEqn,
    context: jax_core.JaxprPpContext,
    settings: jax_core.JaxprPpSettings,
):
  src, dst, *flat_args = eqn.invars
  src_transforms_treedef = eqn.params["src_transforms_treedef"]
  dst_transforms_treedef = eqn.params["dst_transforms_treedef"]
  pp_params = {}
  if not (commit_group := eqn.params["commit_group"]):
    pp_params["commit_group"] = commit_group
  if eqn.params["has_user_predicate"]:
    flat_args, user_predicate = flat_args[:-1], flat_args[-1]
    pp_params["user_predicate"] = user_predicate.pretty_print(context)
  if reduction_op := eqn.params["reduction_op"]:
    pp_params["reduction_op"] = reduction_op
  flat_src_transforms, flat_dst_transforms = util.split_list(
      flat_args,
      [src_transforms_treedef.num_leaves],
  )
  src_transforms = src_transforms_treedef.unflatten(flat_src_transforms)
  dst_transforms = dst_transforms_treedef.unflatten(flat_dst_transforms)
  return pp.concat([
      pp.text("copy_smem_to_gmem"),
      jax_core.pp_kv_pairs(pp_params.items(), context, settings),
      pp.text(" "),
      state_primitives.pp_ref_transforms(context, src, src_transforms),
      pp.text(" -> "),
      state_primitives.pp_ref_transforms(context, dst, dst_transforms),
  ])

