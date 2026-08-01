
def _platforms_for_eqn_ctx(eqn_ctx: core.JaxprEqnContext | None
                           ) -> tuple[str, ...]:
  """Returns platforms to override based on compute type of jaxpr equation."""
  if eqn_ctx is None:
    return ()
  if eqn_ctx.compute_type == 'device_host':
    return ('cpu',)
  if eqn_ctx.compute_type == 'tpu_sparsecore':
    return ('tpu',)
  return ()

