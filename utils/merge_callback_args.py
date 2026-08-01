
def merge_callback_args(in_tree, dyn_args, static_args):
  static_args_dict = dict(static_args)
  all_args = [None] * (len(static_args) + len(dyn_args))
  di = iter(dyn_args)
  for i in range(len(all_args)):
    if i in static_args_dict:
      all_args[i] = static_args_dict[i]
    else:
      all_args[i] = next(di)
  assert next(di, None) is None
  return tree_util.tree_unflatten(in_tree, all_args)

