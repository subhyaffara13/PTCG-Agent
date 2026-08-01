
def _precv_abstract_eval(
    token, *, out_shape, axis_name, **params
):
  return out_shape, {*map(core.NamedAxisEffect, axis_name),
                     single_side_collective_effect}

