
def _call_hi_primitive_linearized_abstract_eval(*_args, _prim, residuals_tree, nz_in_flat):
  return [t.to_tangent_aval() for t in _prim.out_avals_flat]  # TODO(dougalm): handle nonzeros

