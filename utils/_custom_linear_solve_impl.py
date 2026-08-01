
def _custom_linear_solve_impl(*args, const_lengths, jaxprs):
  params, b = _split_linear_solve_args(args, const_lengths)
  x = core.jaxpr_as_fun(jaxprs.solve)(*(params.solve + b))
  return x

