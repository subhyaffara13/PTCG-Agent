
def _psend_abstract_eval(x, *, axis_name, **params):
  _check_axis_names(axis_name, 'psend')
  return abstract_token, {
      *map(core.NamedAxisEffect, axis_name),
      single_side_collective_effect,
  }

