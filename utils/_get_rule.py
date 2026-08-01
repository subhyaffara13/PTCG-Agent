
def _get_rule(ctx: Context, ref, *args, tree):
  ref_aval, *_ = ctx.avals_in
  if not _is_fusion_type(ref_aval):
    return state_primitives.get_p.bind(ref, *args, tree=tree)
  return ref_aval.dtype.get(ref, *args, tree=tree)

