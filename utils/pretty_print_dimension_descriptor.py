
def pretty_print_dimension_descriptor(
    args_kwargs_tree: tree_util.PyTreeDef,
    flat_arg_idx: int, dim_idx: int | None) -> str:
  arg_str = _cached_pretty_print_dimension_descriptor(args_kwargs_tree, flat_arg_idx)
  if dim_idx is not None:
    arg_str += f".shape[{dim_idx}]"
  return arg_str

