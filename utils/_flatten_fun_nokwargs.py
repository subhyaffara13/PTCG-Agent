
def _flatten_fun_nokwargs(f: Callable,
                          store: lu.Store, in_tree: PyTreeDef,
                          *args_flat):
  py_args = tree_unflatten(in_tree, args_flat)
  ans = f(*py_args)
  ans_flat, ans_tree = tree_flatten(ans)
  ans_avals = [core.typeof(x) for x in ans_flat]
  store.store((ans_tree, ans_avals, ()))
  return ans_flat

