
def _custom_jvp_call_push_rule(
    ctx, *block_specs, call_jaxpr: core.ClosedJaxpr, **_
):
  assert not call_jaxpr.consts
  return _push_block_spec_jaxpr(call_jaxpr.jaxpr, *block_specs)

