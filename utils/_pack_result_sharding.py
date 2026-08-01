
def _pack_result_sharding(shape, result_shardings):
  if shape.is_tuple():
    return xc.HloSharding.tuple_sharding(shape, result_shardings)
  else:
    return result_shardings[0]

