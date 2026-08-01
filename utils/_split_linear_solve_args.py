
def _split_linear_solve_args(args, const_lengths):
  params_list = split_list(args, list(const_lengths))
  return _LinearSolveTuple(*params_list[:-1]), params_list[-1]

