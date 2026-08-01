
def _custom_partitioning_impl(*args, call, in_tree, out_tree,
                              propagate_user_sharding,
                              partition, infer_sharding_from_operands,
                              decode_shardings, sharding_rule, static_args):
  del in_tree, out_tree, propagate_user_sharding, partition
  del infer_sharding_from_operands, decode_shardings, static_args, sharding_rule
  return core.jaxpr_as_fun(call)(*args)

