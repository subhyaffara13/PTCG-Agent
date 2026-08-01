
def _copy_gmem_to_smem_pp_eqn(
    eqn: jax_core.JaxprEqn,
    context: jax_core.JaxprPpContext,
    settings: jax_core.JaxprPpSettings,
):
  src, dst, barrier, *flat_args = eqn.invars
  src_transforms_treedef = eqn.params["src_transforms_treedef"]
  dst_transforms_treedef = eqn.params["dst_transforms_treedef"]
  barrier_transforms_treedef = eqn.params["barrier_transforms_treedef"]
  pp_params = {}
  if collective_axes := eqn.params["collective_axes"]:
    pp_params["collective_axes"] = collective_axes
  flat_src_transforms, flat_dst_transforms, flat_barrier_transforms = (
      util.split_list(
          flat_args,
          [
              src_transforms_treedef.num_leaves,
              dst_transforms_treedef.num_leaves,
          ],
      )
  )
  src_transforms = src_transforms_treedef.unflatten(flat_src_transforms)
  dst_transforms = dst_transforms_treedef.unflatten(flat_dst_transforms)
  barrier_transforms = barrier_transforms_treedef.unflatten(
      flat_barrier_transforms
  )
  return pp.concat([
      pp.text("copy_gmem_to_smem"),
      jax_core.pp_kv_pairs(pp_params.items(), context, settings),
      pp.text(" "),
      state_primitives.pp_ref_transforms(context, src, src_transforms),
      pp.text(" -> "),
      state_primitives.pp_ref_transforms(context, dst, dst_transforms),
      pp.text(" using "),
      state_primitives.pp_ref_transforms(context, barrier, barrier_transforms),
  ])

