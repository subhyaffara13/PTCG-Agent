
def broadcasting_vmap(fun, in_axes=0, out_axes=0):
  @functools.wraps(fun)
  def batched_fun(*args):
    args_flat, in_tree  = tree_util.tree_flatten(args)
    in_axes_flat = flatten_axes("vmap in_axes", in_tree, in_axes, kws=False)
    size = max(arg.shape[i] for arg, i in safe_zip(args_flat, in_axes_flat) if i is not None)
    if size > 1:
      if any(i is not None and arg.shape[i] not in (1, size)
             for arg, i in safe_zip(args_flat, in_axes_flat)):
        raise ValueError("broadcasting_vmap: mismatched input shapes")
      args_flat, in_axes_flat = zip(*(
          (arg, None) if i is None else (lax.squeeze(arg, (i,)), None) if arg.shape[i] == 1 else (arg, i)
          for arg, i in zip(args_flat, in_axes_flat)
      ))
    new_args = tree_util.tree_unflatten(in_tree, args_flat)
    new_in_axes = tree_util.tree_unflatten(in_tree, in_axes_flat)
    return vmap(fun, in_axes=new_in_axes, out_axes=out_axes)(*new_args)
  return batched_fun

