
def _compute_on_abstract_eval(*in_avals, jaxpr, compute_type, out_memory_spaces,
                              compiler_options_json):
  out_avals = [a.update(memory_space=s)
               for a, s in zip(jaxpr.out_avals, out_memory_spaces)]
  return out_avals, core.positional_effects(jaxpr)

