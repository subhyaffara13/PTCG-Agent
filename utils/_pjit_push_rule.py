
def _pjit_push_rule(ctx, *block_specs, jaxpr: core.ClosedJaxpr, **_):
  assert not jaxpr.consts
  return _push_block_spec_jaxpr(jaxpr.jaxpr, *block_specs)

