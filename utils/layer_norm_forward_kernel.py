
def layer_norm_forward_kernel(
    x_ref, weight_ref, bias_ref, # Input arrays
    o_ref, mean_ref=None, rstd_ref=None, # Output arrays
    *, eps: float, block_size: int):
  n_col = x_ref.shape[0]

  def mean_body(i, acc):
    col_idx = i * block_size + jnp.arange(block_size)
    mask = col_idx < n_col
    a = plgpu.load(
        x_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    return acc + a

  mean = lax.fori_loop(
      0,
      pl.cdiv(n_col, block_size),
      mean_body,
      init_val=jnp.zeros(block_size),
  ).sum()
  mean /= n_col

  def var_body(i, acc):
    col_idx = i * block_size + jnp.arange(block_size)
    mask = col_idx < n_col
    a = plgpu.load(
        x_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_last"
    ).astype(jnp.float32)
    a = jnp.where(mask, a - mean, 0.)
    return acc + a * a

  var = lax.fori_loop(
      0,
      pl.cdiv(n_col, block_size),
      var_body,
      init_val=jnp.zeros(block_size),
  ).sum()
  var /= n_col
  rstd = 1 / jnp.sqrt(var + eps)
  if mean_ref is not None:
    mean_ref[...] = mean.astype(mean_ref.dtype)
  if rstd_ref is not None:
    rstd_ref[...] = rstd.astype(rstd_ref.dtype)

  @pl.loop(0, pl.cdiv(n_col, block_size))
  def body(i):
    col_idx = i * block_size + jnp.arange(block_size)
    mask = col_idx < n_col
    weight = plgpu.load(weight_ref.at[col_idx], mask=mask)
    bias = plgpu.load(bias_ref.at[col_idx], mask=mask)
    x = plgpu.load(
        x_ref.at[col_idx], mask=mask, other=0.0, eviction_policy="evict_first"
    ).astype(jnp.float32)
    out = (x - mean) * rstd * weight + bias
    plgpu.store(o_ref.at[col_idx], out.astype(o_ref.dtype), mask=mask)

