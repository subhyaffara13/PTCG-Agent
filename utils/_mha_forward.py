
def _mha_forward(
    q,
    k,
    v,
    segment_ids: jax.Array | None,
    sm_scale: float,
    causal: bool,
    block_sizes: BlockSizes,
    backward_pass_impl: str,
    num_warps: int | None,
    num_stages: int,
    grid: Any,
    interpret: bool,
    debug: bool,
    return_residuals: bool,
):
  out, lse = mha(q, k, v, segment_ids=segment_ids, sm_scale=sm_scale,
                 causal=causal, block_sizes=block_sizes,
                 backward_pass_impl=backward_pass_impl,
                 num_warps=num_warps, num_stages=num_stages,
                 grid=grid, interpret=interpret, debug=debug,
                 return_residuals=True)
  residuals = (q, k, v, segment_ids, out, lse)
  ret = (out, lse) if return_residuals else out
  return ret, residuals

