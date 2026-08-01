
def _custom_fusion_effectful_abstract_eval(
    *args,
    jaxpr: core.Jaxpr,
    pallas_jaxpr: core.Jaxpr | None,
    **_):
  del args
  # TODO(jburnim): Error if pallas_jaxpr has different number of outputs, or
  # different shapes and types of outputs?
  if jaxpr.effects:
    raise NotImplementedError(
        "custom_fusion-decorated function {jaxpr.debug_info.func_src_info} "
        "has effects, which is not yet supported: {jaxpr.effects}")
  if pallas_jaxpr is not None and pallas_jaxpr.effects:
    raise NotImplementedError(
        "custom_fusion-decorated function {jaxpr.debug_info.func_src_info} "
        "has a pallas_impl with effects, which is not yet supported: "
        f"{pallas_jaxpr.effects}")
  return jaxpr.out_avals, jaxpr.effects

