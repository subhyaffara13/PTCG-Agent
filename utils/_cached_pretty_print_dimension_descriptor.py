
def _cached_pretty_print_dimension_descriptor(
    args_kwargs_tree: tree_util.PyTreeDef,
    flat_arg_idx: int) -> str:
  args_kwargs_with_paths, _ = tree_util.tree_flatten_with_path(
      args_kwargs_tree.unflatten((0,) * args_kwargs_tree.num_leaves))
  arg_str = args_kwargs_path_to_str(args_kwargs_with_paths[flat_arg_idx][0])
  return arg_str

