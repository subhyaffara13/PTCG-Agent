
def flatten_fun(f: Callable, store: lu.Store,
                in_tree: PyTreeDef, *args_flat):
  py_args, py_kwargs = tree_unflatten(in_tree, args_flat)
  ans = f(*py_args, **py_kwargs)
  ans, out_tree = tree_flatten(ans)
  store.store(out_tree)
  return ans

