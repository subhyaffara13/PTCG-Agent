
def _vmappable_softmax_kernel(
    # inputs
    input_ref,
    # outputs
    probs_ref,
    *,
    # block information
    # It is assumed that block_row >= row_len
    block_row: int,
):
  row_len = input_ref.shape[-1]

  mask = jnp.arange(block_row) < row_len
  row = plgpu.load(
      input_ref.at[pl.ds(0, block_row)], mask=mask, other=-float("inf")
  )

  row_max = jnp.max(row, axis=0)
  numerator = jnp.exp((row - row_max).astype(jnp.float32))
  denominator = jnp.sum(numerator, axis=0)

  plgpu.store(
      probs_ref.at[pl.ds(0, block_row)],
      (numerator / denominator).astype(probs_ref.dtype),
      mask=mask
  )

