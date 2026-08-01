
def args_kwargs_path_to_str(path: tree_util.KeyPath) -> str:
  # String description of `args` or `kwargs`, assuming the path for a tree for
  # the tuple `(args, kwargs)`.
  if path[0] == tree_util.SequenceKey(0):
    return f"args{tree_util.keystr(path[1:])}"
  elif path[0] == tree_util.SequenceKey(1):
    return f"kwargs{tree_util.keystr(path[1:])}"
  else:
    assert False

