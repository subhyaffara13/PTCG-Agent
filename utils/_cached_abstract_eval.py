
def _cached_abstract_eval(primitive: core.Primitive, *aval_qdds, **params):
  return primitive.abstract_eval(*aval_qdds, **params)

