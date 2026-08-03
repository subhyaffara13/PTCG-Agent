from typing import Callable

def flatten_fun_for_vmap(f: Callable,
                         store: lu.Store, in_tree: PyTreeDef, *args_flat):
  py_args, py_kwargs = tree_unflatten(in_tree, args_flat)
  ans = f(*py_args, **py_kwargs)
  ans, out_tree = tree_flatten(ans, is_leaf=is_vmappable)
  store.store(out_tree)
  return ans

