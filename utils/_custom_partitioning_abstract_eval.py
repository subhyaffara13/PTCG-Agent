
def _custom_partitioning_abstract_eval(*avals, call, in_tree, out_tree,
                                       propagate_user_sharding, partition,
                                       infer_sharding_from_operands,
                                       decode_shardings,
                                       sharding_rule,
                                       static_args):
  del in_tree, out_tree, propagate_user_sharding, partition
  del infer_sharding_from_operands, decode_shardings, sharding_rule
  del static_args
  return call.out_avals

