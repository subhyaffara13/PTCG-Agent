
def _pmin_pmax_abstract_eval(name, aval, *, axes, axis_index_groups):
  if not config._check_vma.value:
    return _allreduce_effectful_abstract_eval(
        aval, axes=axes, axis_index_groups=axis_index_groups)
  return _psum_invariant_abstract_eval(name, aval, axes=axes)

