
def manual_rule(prim, vma_rule, ur_rule, multi_out, *avals, **kwargs):
  out_vma = vma_rule(*avals, **kwargs)
  num_out = len(out_vma) if multi_out else None
  if mesh_lib.get_abstract_mesh().are_all_axes_manual:
    out_s = None if num_out is None else [None] * num_out
    out_unreduced, out_reduced = call_ur_rule(
        prim, ur_rule, out_s, num_out, *avals, **kwargs)
  else:
    # TODO(yashkatariya): Handle partial manual unreduced/reduced.
    out_unreduced, out_reduced = (
        (frozenset(), frozenset()) if num_out is None else
        ([frozenset()] * num_out, [frozenset()] * num_out))
  if num_out is None:
    return core.ManualAxisType(varying=out_vma, unreduced=out_unreduced,
                               reduced=out_reduced)
  else:
    return [core.ManualAxisType(varying=v, unreduced=u, reduced=r)
            for v, u, r in zip(out_vma, out_unreduced, out_reduced)]

