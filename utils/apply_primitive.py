
def apply_primitive(prim, *args, **params):
  """Impl rule that compiles and runs a single primitive 'prim' using XLA."""
  fun = xla_primitive_callable(prim, **params)
  # TODO(yashkatariya): Investigate adding is_primitive to jit and never
  # triggering the disable jit path instead of messing around with it here.
  prev = config.disable_jit.swap_local(False)
  try:
    outs = fun(*args)
  finally:
    config.disable_jit.set_local(prev)
  return outs

