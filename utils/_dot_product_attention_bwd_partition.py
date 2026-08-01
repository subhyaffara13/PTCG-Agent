
def _dot_product_attention_bwd_partition(
    scale, seed, dropout_rate, variadic_args, mask_type, layout,
    sliding_window_length, mesh, arg_shapes, result_shape):
  out_shardings = _infer_bwd_output_sharding(mesh, arg_shapes, layout, variadic_args)
  # args sharding
  arg_shardings = [arg_i.sharding for arg_i in arg_shapes]
  # grad_output (index 12) may be inferred as replicated (e.g. when it
  # originates from a broadcast in jnp.sum's backward pass). The cuDNN
  # backward custom-call is lowered with batch size B taken from the
  # partitioned query, so every operand that carries a batch dimension
  # must be partitioned identically. Force fwd_output (11) and
  # grad_output (12) to match query's sharding so the SPMD partitioner
  # slices them to the correct per-shard shape.
  # See https://github.com/jax-ml/jax/issues/25986
  query_sharding = arg_shardings[0]
  arg_shardings[11] = query_sharding # fwd_output
  arg_shardings[12] = query_sharding # grad_output
  arg_shardings = tuple(arg_shardings)
  def sharded_impl(*args):
    impl = functools.partial(
      _dot_product_attention_bwd_impl,
      scale=scale,
      seed=seed,
      dropout_rate=dropout_rate,
      variadic_args=variadic_args,
      mask_type=mask_type,
      layout=layout,
      sliding_window_length=sliding_window_length,
    )
    grads = impl(*args)
    _, has_dbias = variadic_args
    if has_dbias:
      query_spec = arg_shardings[0].spec
      bias_spec = arg_shardings[3].spec
      if layout == AttentionLayout.BNTH.value:
        q_batch_spec, q_num_head_spec, _, _ = query_spec
      else:
        q_batch_spec, _, q_num_head_spec, _ = query_spec
      b_batch_spec, b_num_head_spec, _, _ = bias_spec

      dbias = grads[3]
      if q_batch_spec is not None and b_batch_spec is None:
        # bias is replicated alone batch dim
        dbias = lax_parallel.psum(dbias, q_batch_spec)
      if q_num_head_spec is not None and b_num_head_spec is None:
        # bias is replicated alone num_head dim
        dbias = lax_parallel.psum(dbias, q_num_head_spec)
      grads = grads[:3] + [dbias]
    return grads
  return mesh, sharded_impl, out_shardings, arg_shardings

