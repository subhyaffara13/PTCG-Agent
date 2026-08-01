
def _fused_transpose(cts_in, *primals_in, jaxpr, out_spaces):
  in_flat, in_tree = tree_flatten((primals_in, cts_in))
  in_avals = [typeof(x).update(memory_space=core.MemorySpace.Any)
              for x in in_flat]
  trans_jaxpr, out_tree = _transpose_jaxpr(jaxpr, in_tree, (*in_avals,))
  in_spaces = [x.aval.memory_space if isinstance(x, ad.UndefinedPrimal)
               else typeof(x).memory_space for x in primals_in]
  cts_out_ = tree_unflatten(out_tree, trans_jaxpr.out_avals)
  trans_spaces = tuple(s for x, s in zip(cts_out_, in_spaces) if x)
  cts_out = fused_p.bind(*in_flat, jaxpr=trans_jaxpr, out_spaces=trans_spaces)
  return tree_unflatten(out_tree, cts_out)

