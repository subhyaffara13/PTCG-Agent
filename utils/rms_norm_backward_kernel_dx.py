
def rms_norm_backward_kernel_dx(
    # Inputs
    x_ref, weight_ref, bias_ref, do_ref,
    rstd_ref,
    # Outputs
    dx_ref,
    *, eps: float, block_size: int):
  n_col = x_ref.shape[0]

  def mean_body(i, c1_acc):
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
    a_hat = a * rstd_ref[...]
    wdout = weight * dout
    return c1_acc + a_hat * wdout

  c1 = lax.fori_loop(
      0, pl.cdiv(n_col, block_size), mean_body, jnp.zeros(block_size)
  )
  c1 = c1.sum() / n_col

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
    a_hat = a * rstd_ref[...]
    wdout = weight * dout
    da = (wdout - (a_hat * c1)) * rstd_ref[...]
    plgpu.store(dx_ref.at[col_idx], da.astype(dx_ref.dtype), mask=mask)

