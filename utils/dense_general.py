
def dense_general(
  scope,
  inputs,
  features,
  axis=-1,
  batch_dims=(),
  bias=True,
  dtype=jnp.float32,
  kernel_init=default_kernel_init,
  bias_init=initializers.zeros_init(),
  precision=None,
):
  """Applies a linear transformation to the inputs along multiple dimensions.

  Args:
    inputs: The nd-array to be transformed.
    features: tuple with numbers of output features.
    axis: tuple with axes to apply the transformation on.
    batch_dims: tuple with batch axes.
    bias: whether to add a bias to the output (default: True).
    dtype: the dtype of the computation (default: float32).
    kernel_init: initializer function for the weight matrix.
    bias_init: initializer function for the bias.
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.
  Returns:
    The transformed input.
  """
  inputs = jnp.asarray(inputs, dtype)

  if not isinstance(features, Iterable):
    features = (features,)
  if not isinstance(axis, Iterable):
    axis = (axis,)
  if not isinstance(batch_dims, Iterable):
    batch_dims = (batch_dims,)
  features, axis, batch_dims = tuple(features), tuple(axis), tuple(batch_dims)

  if batch_dims:
    max_dim = np.max(batch_dims)
    if set(batch_dims) != set(range(max_dim + 1)):
      raise ValueError(
        'batch_dims %s must be consecutive leading '
        'dimensions starting from 0.' % str(batch_dims)
      )

  ndim = inputs.ndim
  n_batch_dims = len(batch_dims)
  axis = _normalize_axes(axis, ndim)
  batch_dims = _normalize_axes(batch_dims, ndim)
  n_axis, n_features = len(axis), len(features)

  def kernel_init_wrap(rng, shape, dtype=jnp.float32):
    size_batch_dims = np.prod(shape[:n_batch_dims], dtype=np.int32)
    flat_shape = (
      np.prod(shape[n_batch_dims : n_axis + n_batch_dims]),
      np.prod(shape[-n_features:]),
    )
    kernel = jnp.concatenate(
      [kernel_init(rng, flat_shape, dtype) for _ in range(size_batch_dims)],
      axis=0,
    )
    return jnp.reshape(kernel, shape)

  batch_shape = tuple(inputs.shape[ax] for ax in batch_dims)
  kernel_shape = tuple(inputs.shape[ax] for ax in axis) + features
  kernel = scope.param('kernel', kernel_init_wrap, batch_shape + kernel_shape)
  kernel = jnp.asarray(kernel, dtype)

  batch_ind = tuple(range(n_batch_dims))
  contract_ind = tuple(range(n_batch_dims, n_axis + n_batch_dims))
  out = lax.dot_general(
    inputs,
    kernel,
    ((axis, contract_ind), (batch_dims, batch_ind)),
    precision=precision,
  )
  if bias:

    def bias_init_wrap(rng, shape, dtype=jnp.float32):
      size_batch_dims = np.prod(shape[:n_batch_dims], dtype=np.int32)
      flat_shape = (np.prod(shape[-n_features:]),)
      bias = jnp.concatenate(
        [bias_init(rng, flat_shape, dtype) for _ in range(size_batch_dims)],
        axis=0,
      )
      return jnp.reshape(bias, shape)

    bias = scope.param('bias', bias_init_wrap, batch_shape + features)

    # Reshape bias for broadcast.
    expand_dims = sorted(set(range(inputs.ndim)) - set(axis) - set(batch_dims))
    for ax in expand_dims:
      bias = jnp.expand_dims(bias, ax)
    bias = jnp.asarray(bias, dtype)
    out = out + bias
  return out

