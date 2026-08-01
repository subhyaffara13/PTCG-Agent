
def layer_norm_backward_kernel_dw_db(
    # Inputs
    x_ref, weight_ref, bias_ref, do_ref,
    mean_ref, rstd_ref,
    # Outputs
    dw_ref, db_ref,
    *, eps: float, block_m: int, block_n: int):
  m, n_col = x_ref.shape
  j = pl.program_id(0)
  col_idx = j * block_n + jnp.arange(block_n)
  col_mask = col_idx < n_col

  def body(i, acc):
    row_idx = i * block_m + jnp.arange(block_m)
    row_mask = row_idx < m
    mask = row_mask[:, None] & col_mask[None, :]
    a = plgpu.load(
        x_ref.at[row_idx[:, None], col_idx[None]], mask=mask, other=0.0
    ).astype(jnp.float32)
    dout = plgpu.load(
        do_ref.at[row_idx[:, None], col_idx[None]], mask=mask, other=0.0
    ).astype(jnp.float32)
    mean = plgpu.load(mean_ref.at[row_idx], mask=row_mask, other=0.0).astype(
        jnp.float32
    )
    rstd = plgpu.load(rstd_ref.at[row_idx], mask=row_mask, other=0.0).astype(
        jnp.float32
    )
    a_hat = (a - mean[:, None]) * rstd[:, None]
    dw_acc_ref, db_acc_ref = acc
    return dw_acc_ref + (dout * a_hat).sum(axis=0), db_acc_ref + dout.sum(
        axis=0
    )

  dw_acc, db_acc = lax.fori_loop(
      0,
      pl.cdiv(m, block_m),
      body,
      init_val=(jnp.zeros(block_n), jnp.zeros(block_n)),
  )
  plgpu.store(dw_ref.at[col_idx], dw_acc.astype(dw_ref.dtype), mask=col_mask)
  plgpu.store(db_ref.at[col_idx], db_acc.astype(db_ref.dtype), mask=col_mask)

