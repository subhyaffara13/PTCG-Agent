
def flatten_fun_output(f, store, *args):
  ans = f(*args)
  ans, out_tree = tree_flatten(ans)
  store.store(out_tree)
  return ans

