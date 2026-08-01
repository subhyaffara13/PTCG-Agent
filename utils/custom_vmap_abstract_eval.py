
def custom_vmap_abstract_eval(*in_avals, call, **_):
  del in_avals
  return call.out_avals, call.effects

