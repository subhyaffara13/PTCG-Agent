
def xla_primitive_callable(prim: core.Primitive, **params):
  util.test_event("xla_primitive_callable_cache_miss")
  def prim_fun(*args):
    with config.eager_constant_folding(False):
      return prim.bind(*args, **params)
  prim_fun.__name__ = prim.name
  prim_fun.__qualname__ = prim.name
  prim_fun._apply_primitive = True  # pyrefly: ignore[missing-attribute]
  return api.jit(prim_fun)

