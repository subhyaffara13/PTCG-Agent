
def shape_normalization(x, dimension_numbers):
  """
  Normalizes the shape of the input tensor `x` to `(B, M, K)`.

  This function rearranges and reshapes the input tensor `x` such that:
  - `B` represents the batch dimensions.
  - `M` represents the non-contracting dimensions.
  - `K` represents the contracting dimensions.

  The dimensions are reordered and reshaped based on the provided
  `dimension_numbers`.

  Parameters:
      x: The input tensor to normalize.
      dimension_numbers: A tuple containing two elements:
        - `batch_dims` (tuple): The dimensions of `x` to be treated as batch
          dimensions.
        - `contracting_dims` (tuple): The dimensions of `x` to be treated as
          contracting dimensions.

  Returns:
      jax.numpy.ndarray: The reshaped tensor with shape `(B, M, K)`
  """

  orig_order = list(range(x.ndim))
  contracting_dims, batch_dims = dimension_numbers
  contracting_order = [d for d in orig_order if d in contracting_dims]
  batch_order = [d for d in orig_order if d in batch_dims]
  non_contracting_order = [
      d
      for d in orig_order
      if d not in contracting_dims and d not in batch_dims
  ]
  batch_shape = [x.shape[d] for d in batch_order]
  rows_shape = [x.shape[d] for d in non_contracting_order]
  cols_shape = [x.shape[d] for d in contracting_order]
  new_order = batch_order + non_contracting_order + contracting_order
  rows, cols, batches = (
      np.prod(rows_shape),
      np.prod(cols_shape),
      np.prod(batch_shape, dtype=int),
  )
  t = jnp.transpose(x, new_order)
  return jnp.reshape(t, (batches, rows, cols))

