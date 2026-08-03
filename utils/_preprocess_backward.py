import functools

def _preprocess_backward(out, do, lse, block_q: int,
                         debug: bool, interpret: bool):
  batch_size, seq_len, num_heads, head_dim = out.shape
  head_dim_padded = pl.next_power_of_2(head_dim)
  out_shape = jax.ShapeDtypeStruct.like(lse)
  delta = pl.pallas_call(
      functools.partial(_preprocess_backward_kernel, head_dim=head_dim),
      grid=(pl.cdiv(seq_len, block_q), batch_size, num_heads),
      in_specs=[
          pl.BlockSpec((None, block_q, None, head_dim_padded),
                       lambda i, j, k: (j, i, k, 0)),
          pl.BlockSpec((None, block_q, None, head_dim_padded),
                       lambda i, j, k: (j, i, k, 0)),
      ],
      out_specs=pl.BlockSpec((None, None, block_q), lambda i, j, k: (j, k, i)),
      compiler_params=plgpu.CompilerParams(num_warps=4, num_stages=3),
      out_shape=out_shape,
      debug=debug,
      interpret=interpret,
      name="mha_preprocess_backward",
  )(out, do)
  return delta

