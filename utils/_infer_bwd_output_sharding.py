
def _infer_bwd_output_sharding(mesh, arg_shapes, layout, variadic_args):
  # (*batch, q_seq, num_head, head)
  query_spec = _get_padded_spec(arg_shapes[0])
  # (*batch, kv_seq, num_head, head)
  key_spec = _get_padded_spec(arg_shapes[1])
  value_spec = _get_padded_spec(arg_shapes[2])
  has_bias, has_dbias = variadic_args
  bias_spec = _get_padded_spec(arg_shapes[3]) if has_bias else None
  _check_qkv_bias_mask_spec(
    query_spec, key_spec, value_spec, bias_spec, layout)
  # keep grad query sharding same as query sharding
  grad_query_sharding = NamedSharding(mesh, PartitionSpec(*query_spec))
  grad_key_sharding = NamedSharding(mesh, PartitionSpec(*key_spec))
  grad_value_sharding = NamedSharding(mesh, PartitionSpec(*key_spec))
  out_shardings = [grad_query_sharding, grad_key_sharding, grad_value_sharding]
  if has_dbias:
    assert bias_spec is not None
    grad_bias_sharding = NamedSharding(mesh, PartitionSpec(*bias_spec))
    out_shardings = out_shardings + [grad_bias_sharding]
  return out_shardings

