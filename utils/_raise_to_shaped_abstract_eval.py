
def _raise_to_shaped_abstract_eval(x, *, axis_name, **params):
  _check_axis_names(axis_name, 'ppermute')
  collective_vma_rule('ppermute', axis_name, x)
  check_unreduced_args([x], axis_name, 'ppermute')
  return x

