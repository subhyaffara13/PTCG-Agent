
def _split_root_args(args, const_lengths):
  params_list = split_list(args, list(const_lengths))
  return _RootTuple(*params_list[:-1]), params_list[-1]

