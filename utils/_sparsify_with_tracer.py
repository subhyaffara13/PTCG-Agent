
def _sparsify_with_tracer(fun: Callable):
  """Implementation of sparsify() using tracers."""
  @functools.wraps(fun)
  def _wrapped(*args):
    args_flat, in_tree = tree_flatten(args, is_leaf=_is_sparse_obj)
    wrapped_fun, out_tree = flatten_fun_nokwargs(
        lu.wrap_init(fun,
                     debug_info=api_util.debug_info("sparsify", fun, args, {})),
        in_tree)
    out = sparsify_fun(wrapped_fun, args_flat)
    return tree_unflatten(out_tree(), out)
  return _wrapped

