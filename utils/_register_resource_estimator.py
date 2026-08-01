
def _register_resource_estimator(primitive: jax_core.Primitive):
  def deco(fn):
    _resource_estimators[primitive] = fn
    return fn

  return deco

