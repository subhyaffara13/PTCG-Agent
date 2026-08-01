
def _custom_root(const_lengths, jaxprs, *args):
  params, initial_guess = _split_root_args(args, const_lengths)
  solution = core.jaxpr_as_fun(jaxprs.solve)(*(params.solve + initial_guess))
  return solution

