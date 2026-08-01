
def _estimate_resources(
    ctx: ResourceEstimatorContext, jaxpr: jax_core.Jaxpr
) -> Resources:
  """Estimates the resources required by the kernel."""
  rs = Resources(smem_scratch_bytes=0)
  for eqn in jaxpr.eqns:
    # TODO(slebedev): Add support for other primitives, notably control flow.
    if rule := _resource_estimators.get(eqn.primitive):
      rs = rs.or_(
          rule(ctx, *(invar.aval for invar in eqn.invars), **eqn.params),
          ctx.axis_names,
      )
      continue
    # Assume that unsupported primitives are neutral wrt resource usage,
    # unless they have a jaxpr in their params.
    if any(
        isinstance(v, (jax_core.Jaxpr, jax_core.ClosedJaxpr))
        for v in eqn.params.values()
    ):
      raise NotImplementedError(
          f"Resource estimation does not support {eqn.primitive}"
      )

  return rs

