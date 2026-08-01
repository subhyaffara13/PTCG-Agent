
def _get_fusion_values(
    fusion: Callable,
    args,
    kwargs,
    discharge_refs: bool = False,
    allow_additional_outputs: bool = False
):
  jaxpr, values, _, out_tree = fuser_utils.make_jaxpr(
      fusion, *args, **kwargs
  )
  assert len(values) == len(jaxpr.constvars), (jaxpr, values)

  if any(isinstance(v, jax.ref.Ref) for v in values) and not discharge_refs:
    raise ValueError('Ref values are only supported in get_fusion_values when '
                     'discharge_refs is True.')
  output_input_aliases = {}
  if discharge_refs:
    jaxpr, used_consts, output_input_aliases = fuser_utils.discharge_state(
        jaxpr, allow_additional_outputs=allow_additional_outputs, dce=True)
    values = [v for used, v in zip(used_consts, values) if used]

  out_usages = tuple({Usage.REGULAR} for _ in jaxpr.outvars)
  read_usage_env = compute_usage(jaxpr, out_usages)
  constvar_usages = util.safe_map(read_usage_env, jaxpr.constvars)
  invar_usages = util.safe_map(read_usage_env, jaxpr.invars)
  del invar_usages  # These don't correspond to values
  is_scalar_prefetch = tuple(
      Usage.SCALAR_PREFETCH in usage for usage in constvar_usages
  )
  regular_values, scalar_prefetch_values = util.partition_list(
      is_scalar_prefetch, values
  )

  def new_kernel_fn(values, *args, **kwargs):
    values = util.merge_lists(
        is_scalar_prefetch, values, scalar_prefetch_values
    )
    flat_args, _ = tree_util.tree_flatten((args, kwargs))
    out_flat = core.eval_jaxpr(jaxpr, values, *flat_args)
    if discharge_refs and len(out_flat) > out_tree.num_leaves:
      out_flat, extra_out = util.split_list(out_flat, [out_tree.num_leaves])
      out = tree_util.tree_unflatten(out_tree, out_flat)
      if allow_additional_outputs:
        return out, tuple(extra_out)
      else:
        # TODO(jburnim): Raise an error if an input fusion is modifying a Ref?
        return out
    return tree_util.tree_unflatten(out_tree, out_flat)

  ret = new_kernel_fn, tuple(regular_values), tuple(scalar_prefetch_values)
  if discharge_refs and allow_additional_outputs:
      return (*ret, output_input_aliases)
  return ret

