
def _split_callback_args(args, kwargs):
  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  static_args, dyn_args = {}, []
  for i, a in enumerate(flat_args):
    try:
      core.shaped_abstractify(a)
      dyn_args.append(a)
    except (AssertionError, TypeError):
      static_args[i] = a
  return in_tree, dyn_args, static_args

