
def call_cudnn_fusion(f, *args, **kwargs):
  """Creates a new cudnn_fusion corresponding to calling
  the given function f with args and kwargs."""
  jaxpr, out_shapes = api.make_jaxpr(
    functools.partial(f, **kwargs), return_shape=True
  )(*args)
  flat_args = tree_util.tree_leaves(args)
  out_tree = tree_util.tree_structure(out_shapes)
  out_flat = cudnn_fusion_p.bind(*flat_args, name=f.__name__, jaxpr=jaxpr)
  return tree_util.tree_unflatten(out_tree, out_flat)

