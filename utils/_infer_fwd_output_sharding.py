
def _infer_fwd_output_sharding(mesh, arg_shapes, variadic_args, is_training, layout):
  # only sharding on batch and num_head dim is allowed
  # (*batch, q_seq, num_head, head)
  query_spec = _get_padded_spec(arg_shapes[0])
  # (*batch, kv_seq, num_head, head)
  key_spec = _get_padded_spec(arg_shapes[1])
  value_spec = _get_padded_spec(arg_shapes[2])
  has_bias, _ = variadic_args
  bias_spec = _get_padded_spec(arg_shapes[3]) if has_bias else None

  _check_qkv_bias_mask_spec(
    query_spec, key_spec, value_spec, bias_spec, layout)
  # keep out sharding same as query sharding since they have same shape
  out_sharding = NamedSharding(mesh, PartitionSpec(*query_spec))
  if is_training:
    # activation sharding
    if layout == AttentionLayout.BNTH.value:
      *batch_spec, num_head_spec, q_seq_spec, _ = query_spec
    else:
      *batch_spec, q_seq_spec, num_head_spec, _ = query_spec
    activation_sharding = NamedSharding(
      mesh, PartitionSpec(*batch_spec, num_head_spec, q_seq_spec, None))
    return [out_sharding, activation_sharding]
  return [out_sharding]

