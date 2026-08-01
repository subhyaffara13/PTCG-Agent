
def _check_qkv_bias_mask_spec(
    query_spec, key_spec, value_spec, bias_spec, layout):
  # check qkv spec
  if not query_spec == key_spec == value_spec:
    raise ValueError("Query, key and value should have same sharding.")
  if layout == AttentionLayout.BNTH.value:
    *batch_spec, num_head_spec, q_seq_spec, head_spec = query_spec
  else:
    *batch_spec, q_seq_spec, num_head_spec, head_spec = query_spec
  if q_seq_spec is not None:
    raise ValueError("Sharding on sequence dim is not allowed.")
  if head_spec is not None:
    raise ValueError("Sharding on head dim is not allowed.")
  # check bias spec
  if bias_spec:
    *bias_batch_spec, bias_num_head_spec, bias_q_seq_spec, bias_kv_seq_spec = bias_spec
    if any(bias_batch_spec) and bias_batch_spec != batch_spec or \
      bias_num_head_spec is not None and bias_num_head_spec != num_head_spec:
      raise ValueError(
        "Query and bias should have same sharding on batch and num_head dim.")
    if bias_q_seq_spec is not None or bias_kv_seq_spec is not None:
      raise ValueError("Sharding on bias sequence dim is not allowed.")

