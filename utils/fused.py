
def fused(*, out_spaces):
  def wrap(f):
    def wrapped(*args):
      dbg = debug_info('fused', f, args, {})
      args_flat, in_tree = tree_flatten(args)
      in_avals = [typeof(x).update(memory_space=core.MemorySpace.Any)
                  for x in args_flat]
      jaxpr, out_tree = _trace_to_jaxpr(f, in_tree, tuple(in_avals), dbg)
      outs_flat = fused_p.bind(*args_flat, jaxpr=jaxpr, out_spaces=out_spaces)
      return tree_unflatten(out_tree, outs_flat)
    return wrapped
  return wrap

