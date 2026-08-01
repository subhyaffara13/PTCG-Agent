
def custom_vmap_batching(args_flat, dims, *, call, rule, in_tree, out_tree):
  del call
  axis_size, = {x.shape[d] for x, d in zip(args_flat, dims) if d is not None}
  args_flat = map(maybe_bdim_at_front, args_flat, dims)
  flat_in_batched = [d is not None for d in dims]

  args = tree_unflatten(in_tree, args_flat)
  in_batched = tree_unflatten(in_tree, flat_in_batched)
  out, out_batched = call_rule(rule, axis_size, in_batched, args)
  flat_outs, tree1 = tree_flatten(out)
  flat_out_batched, tree2 = tree_flatten(out_batched)
  check_vmap_rule_trees(rule, out_tree, tree1, tree2)
  flat_out_dims = [0 if b else None for b in flat_out_batched]
  return flat_outs, flat_out_dims

