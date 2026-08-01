
def _custom_vjp_call_typecheck(_, *in_avals, call_jaxpr, **kwargs):
  del in_avals, kwargs
  disallowed_effects = effects.custom_derivatives_allowed_effects.filter_not_in(
      call_jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `custom_vjp`: {disallowed_effects}')
  return call_jaxpr.out_avals, core.positional_effects(call_jaxpr)

