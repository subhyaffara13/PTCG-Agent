
def custom_vmap_impl(*args, call, rule, in_tree, out_tree):
  del rule, in_tree, out_tree
  return core.jaxpr_as_fun(call)(*args)

