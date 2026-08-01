
def conv_transpose(lhs: Array, rhs: Array, strides: Sequence[int],
                   padding: str | Sequence[tuple[int, int]],
                   rhs_dilation: Sequence[int] | None = None,
                   dimension_numbers: ConvGeneralDilatedDimensionNumbers = None,
                   transpose_kernel: bool = False,
                   precision: lax.PrecisionLike = None,
                   preferred_element_type: DTypeLike | None = None,
                   use_consistent_padding: bool = False) -> Array:
  """Convenience wrapper for calculating the N-d convolution "transpose".

  This function directly calculates a fractionally strided conv rather than
  indirectly calculating the gradient (transpose) of a forward convolution.

  Notes:
    TensorFlow/Keras Compatibility: By default, JAX does NOT reverse the
    kernel's spatial dimensions. This differs from TensorFlow's "Conv2DTranspose"
    and similar frameworks, which flip spatial axes and swap input/output channels.

    To match TensorFlow/Keras behavior, set "transpose_kernel=True" .

  Args:
    lhs: a rank `n+2` dimensional input array.
    rhs: a rank `n+2` dimensional array of kernel weights.
    strides: sequence of `n` integers, sets fractional stride.
    padding: 'SAME', 'VALID', or a sequence of `n` integer 2-tuples describing before-and-after
      padding for each spatial dimension. If `use_consistent_padding=True`, this is interpreted
      as the padding of the corresponding forward conv, which effectively adds
      `dilation * (kernel_size - 1) - padding` zero padding to each side
      of the input so that `conv_transpose` becomes the gradient of `conv` when given the same padding
      and stride arguments. This is the behavior in PyTorch. If `use_consistent_padding=False`,
      the 'SAME' and 'VALID' strings are interpreted as the padding of the corresponding forward conv,
      but integer tuples are interpreted as padding for the transposed convolution.
    rhs_dilation: `None`, or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of `rhs`. RHS dilation
      is also known as atrous convolution.
    dimension_numbers: tuple of dimension descriptors as in
      lax.conv_general_dilated. Defaults to tensorflow convention.
    transpose_kernel: if True flips spatial axes and swaps the input/output
      channel axes of the kernel. This makes the output of this function identical
      to the gradient-derived functions like keras.layers.Conv2DTranspose
      applied to the same kernel. For typical use in neural nets this is completely
      pointless and just makes input/output channel specification confusing.
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.
    use_consistent_padding : In older versions of jax, the `padding` argument was interpreted differently
      depending on whether it was a string or a sequence of integers. Strings were interpreted as padding
      for the forward convolution, while integers were interpreted as padding for the transposed convolution.
      If `use_consistent_padding` is False, this inconsistent behavior is preserved for backwards compatibility.
  Returns:
    Transposed N-d convolution, with output padding following the conventions of
    keras.layers.Conv2DTranspose.
  """
  assert len(lhs.shape) == len(rhs.shape) and len(lhs.shape) >= 2
  ndims = len(lhs.shape)
  one = (1,) * (ndims - 2)
  # Set dimensional layout defaults if not specified.
  if dimension_numbers is None:
    if ndims == 2:
      dimension_numbers = ('NC', 'IO', 'NC')
    elif ndims == 3:
      dimension_numbers = ('NHC', 'HIO', 'NHC')
    elif ndims == 4:
      dimension_numbers = ('NHWC', 'HWIO', 'NHWC')
    elif ndims == 5:
      dimension_numbers = ('NHWDC', 'HWDIO', 'NHWDC')
    else:
      raise ValueError('No 4+ dimensional dimension_number defaults.')
  dn = conv_dimension_numbers(lhs.shape, rhs.shape, dimension_numbers)
  k_shape = np.take(rhs.shape, dn.rhs_spec)
  k_sdims = k_shape[2:]
  # Calculate correct output shape given padding and strides.
  if rhs_dilation is None:
    rhs_dilation = (1,) * (rhs.ndim - 2)
  pads: str | Sequence[tuple[int, int]]
  if use_consistent_padding or (isinstance(padding, str) and padding in {'SAME', 'VALID'}):
    effective_k_size = map(lambda k, r: core.dilate_dim(k, r), k_sdims, rhs_dilation)
    replicated_padding = [padding] * len(strides) if isinstance(padding, str) else padding
    pads = tuple(_conv_transpose_padding(k, s, p)
      for k,s,p in zip(effective_k_size, strides, replicated_padding))
  else:
      pads = padding
  if transpose_kernel:
    # flip spatial dims and swap input / output channel axes
    rhs = _flip_axes(rhs, np.array(dn.rhs_spec)[2:])
    rhs = rhs.swapaxes(dn.rhs_spec[0], dn.rhs_spec[1])
  return conv_general_dilated(lhs, rhs, one, pads, strides, rhs_dilation, dn,
                              precision=precision,
                              preferred_element_type=preferred_element_type)


def conv_transpose(
  scope,
  inputs,
  features,
  kernel_size,
  strides=None,
  padding='SAME',
  kernel_dilation=None,
  bias=True,
  dtype=jnp.float32,
  precision=None,
  kernel_init=default_kernel_init,
  bias_init=initializers.zeros_init(),
):
  """Applies a transposed convolution to the inputs. Behaviour mirrors that of
  `jax.lax.conv_transpose`.

  Args:
    scope: functional scope.
    inputs: input data with dimensions (batch, spatial_dims..., features).
    features: number of convolution filters.
    kernel_size: shape of the convolutional kernel.
    strides: a sequence of `n` integers, representing the inter-window
      strides.
    padding: either the string `'SAME'`, the string `'VALID'`, or a sequence
      of `n` `(low, high)` integer pairs that give the padding to apply before
      and after each spatial dimension.
    kernel_dilation: `None`, or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of the convolution
      kernel. Convolution with kernel dilation is also known as 'atrous
      convolution'.
    bias: whether to add a bias to the output (default: True).
    dtype: the dtype of the computation (default: float32).
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.
    kernel_init: initializer for the convolutional kernel.
    bias_init: initializer for the bias.
  Returns:
    The convolved data.
  """
  inputs = jnp.asarray(inputs, dtype)
  strides = strides or (1,) * (inputs.ndim - 2)

  in_features = inputs.shape[-1]
  kernel_shape = kernel_size + (in_features, features)
  kernel = scope.param('kernel', kernel_init, kernel_shape)
  kernel = jnp.asarray(kernel, dtype)

  y = lax.conv_transpose(
    inputs,
    kernel,
    strides,
    padding,
    rhs_dilation=kernel_dilation,
    precision=precision,
  )

  if bias:
    bias = scope.param('bias', bias_init, (features,))
    bias = jnp.asarray(bias, dtype)
    y += jnp.reshape(bias, (1,) * (y.ndim - 1) + (-1,))
  return y

