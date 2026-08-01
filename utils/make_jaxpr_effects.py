
def make_jaxpr_effects(constvars, invars, outvars, eqns) -> effects.Effects:
  jaxpr_effects = set()
  input_vars = {*constvars, *invars}
  mut_arrays = set()
  for eqn in eqns:
    if eqn.primitive.ref_allocating:
      outvar, = eqn.outvars
      mut_arrays.add(outvar)
    for eff in eqn.effects:
      if isinstance(eff, effects.JaxprInputEffect):
        if eff.input in mut_arrays:
          continue
        if eff.input not in input_vars:
          # TODO(mattjj): ask for forgiveness
          dbg = type('Fake', (), {'resolve_result_paths': lambda self_: self_,
                                  'assert_arg_names': lambda _, __: None,
                                  'assert_result_paths': lambda _, __: None,
                                  })()
          raise ValueError(
                f"`JaxprInputEffect` {eff} does not have "
                f"a corresponding jaxpr input."
                f"\n Equation: {eqn}\n"
                f"\n Effects: {eqn.effects}\n"
                "\n Jaxpr: "
                f"{core.Jaxpr(constvars, invars, outvars, eqns, set(), dbg)}")
      jaxpr_effects.add(eff)
  return jaxpr_effects

