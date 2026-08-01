
def batch_jaxpr(closed_jaxpr, axis_data, in_batched, instantiate):
  inst = tuple(instantiate) if isinstance(instantiate, list) else instantiate
  return _batch_jaxpr(closed_jaxpr, axis_data, tuple(in_batched), inst)

