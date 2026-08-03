from typing import Callable

def flatten_fun_nokwargs(f: Callable, store: lu.Store,
                         in_tree: PyTreeDef, *args_flat):
  py_args = tree_unflatten(in_tree, args_flat)
  ans = f(*py_args)
  ans, out_tree = tree_flatten(ans)
  store.store(out_tree)
  return ans

