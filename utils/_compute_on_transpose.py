
def _compute_on_transpose(cts_in, *primals_in, jaxpr, compute_type,
                          out_memory_spaces, compiler_options_json):
  in_flat, in_tree = tree_flatten((primals_in, cts_in))
  in_avals = tuple(core.typeof(x) for x in in_flat)
  trans_jaxpr, out_tree = _transpose_jaxpr(jaxpr, in_avals, in_tree)
  in_spaces = [x.aval.memory_space if isinstance(x, ad.UndefinedPrimal)
               else core.typeof(x).memory_space for x in primals_in]
  cts_out_ = tree_unflatten(out_tree, trans_jaxpr.out_avals)
  trans_spaces = tuple(s for x, s in zip(cts_out_, in_spaces) if x)
  cts_out = compute_on_p.bind(*in_flat, jaxpr=trans_jaxpr,
                              compute_type=compute_type,
                              out_memory_spaces=trans_spaces,
                              compiler_options_json=compiler_options_json)
  return tree_unflatten(out_tree, cts_out)

