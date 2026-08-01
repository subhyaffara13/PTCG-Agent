
def _dynamic_slice_typecheck_rule(_, x, *start_indices, slice_sizes):
  out_aval, effects = dynamic_slice_p.abstract_eval(
      x.aval, *(d.aval for d in start_indices), slice_sizes=slice_sizes)
  return [out_aval], effects

