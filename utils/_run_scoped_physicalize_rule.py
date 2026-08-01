
def _run_scoped_physicalize_rule(
    interpreter, *consts, jaxpr: jax_core.Jaxpr, collective_axes, **params):
  if collective_axes:
    raise NotImplementedError(
        "run_scoped interpret rule does not support collective axes"
    )
  physical_jaxpr, physical_consts = interpreter(jaxpr, consts)
  return primitives.run_scoped_p.bind(
      *physical_consts, jaxpr=physical_jaxpr, collective_axes=collective_axes,
      **params
  )

