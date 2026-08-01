
def _make_1d_grid_from_slice(s: slice, op_name: str) -> Array:
  start = core.concrete_or_error(None, s.start,
                                 f"slice start of jnp.{op_name}") or 0
  stop = core.concrete_or_error(None, s.stop,
                                f"slice stop of jnp.{op_name}")
  step = core.concrete_or_error(None, s.step,
                                f"slice step of jnp.{op_name}") or 1
  if np.iscomplex(step):
    newobj = linspace(start, stop, int(abs(step)))
  else:
    newobj = arange(start, stop, step)

  return newobj

