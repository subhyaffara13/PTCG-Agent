
def _swap_rule(ctx: Context, ref, val, *args, tree):
  ref_aval, *_ = ctx.avals_in
  if not _is_fusion_type(ref_aval):
    return state_primitives.swap_p.bind(ref, val, *args, tree=tree)
  return ref_aval.dtype.swap(ref, val, *args, tree=tree)

