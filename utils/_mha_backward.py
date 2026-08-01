
def _mha_backward(sm_scale: float, causal: bool, block_sizes: BlockSizes,
                  backward_pass_impl: str, num_warps: int | None,
                  num_stages: int, grid: Any, interpret: bool,
                  debug: bool, return_residuals: bool, res, do):
  if return_residuals:
    raise ValueError(
        "Kernel differentiation is not supported if return_residuals is True.")
  q, k, v, segment_ids, out, lse = res
  del num_stages, grid, return_residuals

  if backward_pass_impl == "xla":
    return jax.vjp(
        functools.partial(mha_reference, sm_scale=sm_scale, causal=causal),
        q,
        k,
        v,
        segment_ids,
    )[1](do)
  elif backward_pass_impl == "triton":
    if not block_sizes.has_backward_blocks:
      raise ValueError("Backward block sizes must all be set.")

    assert block_sizes.block_q_dkv is not None
    assert block_sizes.block_kv_dkv is not None
    assert block_sizes.block_q_dq is not None
    assert block_sizes.block_kv_dq is not None

    batch_size, q_seq_len, num_heads, head_dim = q.shape
    kv_seq_len = k.shape[1]
    block_q = min(block_sizes.block_q, q_seq_len)
    block_q_dkv = min(block_sizes.block_q_dkv, q_seq_len)
    block_kv_dkv = min(block_sizes.block_kv_dkv, kv_seq_len)
    block_q_dq = min(block_sizes.block_q_dq, q_seq_len)
    block_kv_dq = min(block_sizes.block_kv_dq, kv_seq_len)
    head_dim_padded = pl.next_power_of_2(head_dim)

    if q_seq_len // block_q_dq != kv_seq_len // block_kv_dkv:
      raise ValueError(
          "q_seq_len and kv_seq_len must be divided into the same "
          "number of blocks for the fused backward pass."
      )

    delta = _preprocess_backward(out, do, lse, block_q, debug, interpret)
    out_shapes = [
        jax.ShapeDtypeStruct.like(q),
        jax.ShapeDtypeStruct.like(k),
        jax.ShapeDtypeStruct.like(v),
    ]

    in_specs: list[pl.BlockSpec | None] = [
        pl.BlockSpec((None, q_seq_len, None, head_dim_padded),
                     lambda i, j, _: (i, 0, j, 0)),
        pl.BlockSpec((None, kv_seq_len, None, head_dim_padded),
                     lambda i, j, _: (i, 0, j, 0)),
        pl.BlockSpec((None, kv_seq_len, None, head_dim_padded),
                     lambda i, j, _: (i, 0, j, 0)),
        pl.BlockSpec((None, q_seq_len, None, head_dim_padded),
                     lambda i, j, _: (i, 0, j, 0)),
        pl.BlockSpec((None, q_seq_len, None, head_dim_padded),
                     lambda i, j, _: (i, 0, j, 0)),
        pl.BlockSpec((None, None, q_seq_len), lambda i, j, _: (i, j, 0)),
        pl.BlockSpec((None, None, q_seq_len), lambda i, j, _: (i, j, 0)),
    ]
    if segment_ids is None:
      in_specs.insert(3, None)
    else:
      in_specs.insert(3, pl.BlockSpec((None, kv_seq_len),
                                      lambda i, j, _: (i, 0)))

    grid = (batch_size, num_heads, pl.cdiv(kv_seq_len, block_kv_dkv))
    num_warps_ = num_warps
    if num_warps_ is None:
      if (
          block_q_dkv * block_kv_dkv < 128 * 128
          or block_q_dq * block_kv_dq < 128 * 128
      ):
        num_warps_ = 4
      else:
        num_warps_ = 8


    dq, dk, dv = pl.pallas_call(
        functools.partial(
            mha_backward_kernel,
            sm_scale=sm_scale,
            causal=causal,
            block_q_dkv=block_q_dkv,
            block_kv_dkv=block_kv_dkv,
            block_q_dq=block_q_dq,
            block_kv_dq=block_kv_dq,
            head_dim=head_dim,
        ),
        out_shape=out_shapes,
        in_specs=in_specs,
        grid=grid,
        out_specs=[
            pl.BlockSpec(
                (None, block_q_dq, None, head_dim_padded),
                lambda i, j, k: (i, k, j, 0),  # dq
            ),
            pl.BlockSpec(
                (None, block_kv_dkv, None, head_dim_padded),
                lambda i, j, k: (i, k, j, 0),  # dk
            ),
            pl.BlockSpec(
                (None, block_kv_dkv, None, head_dim_padded),
                lambda i, j, k: (i, k, j, 0),  # dv
            ),
        ],
        name="mha_backward",
        debug=debug,
        interpret=interpret,
        compiler_params=plgpu.CompilerParams(
            num_warps=num_warps_, num_stages=2
        ),
    )(q, k, v, segment_ids, out, do, lse, delta)
  else:
    raise ValueError(f"Invalid backward pass implementation: {backward_pass_impl}")
  return dq.astype(q.dtype), dk, dv, None

