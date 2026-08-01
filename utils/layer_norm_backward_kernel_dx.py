
def layer_norm_backward_kernel_dx(
    # Inputs
    x_ref, weight_ref, bias_ref, do_ref,
    mean_ref, rstd_ref,
    # Outputs
    dx_ref,
    *, eps: float, block_size: int):
  n_col = x_ref.shape[0]

  def mean_body(i, acc):
    col_idx = i * block_size + jnp.arange(block_size)
    mask = col_idx < n_col
    a = plgpu.load(
        x_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    dout = plgpu.load(
        do_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    weight = plgpu.load(
        weight_ref.at[col_idx],
        mask=mask,
        other=0.0,
        eviction_policy="evict_last",
    ).astype(jnp.float32)
    a_hat = (a - mean_ref[...]) * rstd_ref[...]
    wdout = weight * dout
    mean1_acc, mean2_acc = acc
    return mean1_acc + a_hat * wdout, mean2_acc + wdout
  mean1, mean2 = lax.fori_loop(
      0,
      pl.cdiv(n_col, block_size),
      mean_body,
      init_val=(jnp.zeros(block_size), jnp.zeros(block_size)),
  )
  mean1 = mean1.sum() / n_col
  mean2 = mean2.sum() / n_col

  @pl.loop(0, pl.cdiv(n_col, block_size))
  def dx_body(i):
    col_idx = i * block_size + jnp.arange(block_size)
    mask = col_idx < n_col
    a = plgpu.load(
        x_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    dout = plgpu.load(
        do_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    weight = plgpu.load(
        weight_ref.at[col_idx],
        mask=mask,
        other=0.0,
        eviction_policy="evict_last",
    ).astype(jnp.float32)
    a_hat = (a - mean_ref[...]) * rstd_ref[...]
    wdout = weight * dout
    da = (wdout - (a_hat * mean1 + mean2)) * rstd_ref[...]
    plgpu.store(dx_ref.at[col_idx], da.astype(dx_ref.dtype), mask=mask)

