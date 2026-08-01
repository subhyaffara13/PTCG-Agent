
def get_param_names(fn, n_args):
    if isinstance(fn, OpOverloadPacket):
        fn = fn.op

    if (
        not is_function_or_method(fn)
        and callable(fn)
        and is_function_or_method(fn.__call__)
    ):  # noqa: B004
        # De-sugar calls to classes
        fn = fn.__call__

    if is_function_or_method(fn):
        if is_ignored_fn(fn):
            fn = inspect.unwrap(fn)
        return inspect.getfullargspec(fn).args
    else:
        # The `fn` was not a method or function (maybe a class with a __call__
        # method, so use a default param name list)
        return [str(i) for i in range(n_args)]


def get_param_names(
    item: PyTree, *, include_empty_nodes: bool = True
) -> PyTree:
  """Gets parameter names for PyTree elements."""
  is_leaf = is_empty_or_leaf if include_empty_nodes else None
  return jax.tree_util.tree_map_with_path(
      lambda kp, _: param_name_from_keypath(kp),
      item,
      is_leaf=is_leaf,
  )

