
def conv(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor | tuple[FakeTensor | None, FakeTensor | None, FakeTensor | None]:
    _, new_kwargs = _normalize_function_or_error(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    input_ = new_kwargs["input"]
    weight = new_kwargs["weight"]
    device = input_.fake_device
    # need to re-enable mode so the tensors report fake device
    with fake_mode:
        # if the input is unsqueezed in Convolution.cpp we get segfault
        k = weight.ndim

        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import has_guarding_hint

        all_hinted = all(has_guarding_hint(s) for s in input_.shape) and all(
            has_guarding_hint(s) for s in weight.shape
        )

        if not all_hinted:
            # TODO: We can make this a little more faithful with best effort
            # channels last detection (but only if it's statically obvious!)
            mem_fmt = None
        else:
            # convolution has "bias" but not "bias_sizes"; convolution_backward
            # has "bias_sizes" but not "bias". .get() handles both with one call.
            bias = new_kwargs.get("bias")
            select_kwargs: dict[str, object] = dict(
                stride=new_kwargs["stride"],
                padding=new_kwargs["padding"],
                dilation=new_kwargs["dilation"],
                transposed=new_kwargs["transposed"],
                output_padding=new_kwargs["output_padding"],
                groups=new_kwargs["groups"],
                bias=bias,
            )
            if bias is None:
                select_kwargs["bias_sizes"] = new_kwargs.get("bias_sizes")
            conv_backend = torch._C._select_conv_backend(
                input_, weight, **select_kwargs
            )
            # Expand 1d -> 2d.
            # Note: Avoid expanding before calling _select_conv_backend,
            # as the function handles 2D expansion internally.
            if k == 3 and not input_.is_mkldnn and not input_.is_xpu:
                # Note: Using input.to(memory_format=contiguous) does not work.
                input_ = input_.contiguous().unsqueeze(2)
                weight = weight.unsqueeze(2)
            mem_fmt = torch._C._conv_determine_backend_memory_format(
                input_, weight, conv_backend
            )

    def convert(
        t: torch.Tensor | None, mem_fmt: torch.memory_format | None
    ) -> FakeTensor | None:
        if t is None:
            return t
        if mem_fmt is not None:
            # channels last only support 4d, try to expand dim then convert it back later.
            if t.dim() == 3 and mem_fmt == torch.channels_last:
                t = t.unsqueeze(2).to(memory_format=mem_fmt).squeeze(2)
            else:
                t = t.to(memory_format=mem_fmt)
        return FakeTensor(fake_mode, t, device)

    with in_kernel_invocation_manager(fake_mode):
        out = func(**new_kwargs)

        if func is aten.convolution.default:
            return convert(out, mem_fmt)  # type: ignore[return]
        else:
            return (
                convert(out[0], mem_fmt),
                convert(out[1], mem_fmt),
                convert(out[2], None),
            )


def conv(astr):
    b = astr.split(',')
    l = [x.strip() for x in b]
    for i in range(len(l)):
        m = item_re.match(l[i])
        if m:
            j = int(m.group('index'))
            l[i] = l[j]
    return ','.join(l)


def conv(lhs, rhs, window_strides, padding):
  pads = padtype_to_pads(lhs.shape[2:], rhs.shape[2:], window_strides, padding)
  return _conv(lhs, rhs, window_strides, pads)


def conv(lhs: Array, rhs: Array, window_strides: Sequence[int],
         padding: str, precision: lax.PrecisionLike = None,
         preferred_element_type: DTypeLike | None = None) -> Array:
  """Convenience wrapper around `conv_general_dilated`.

  Args:
    lhs: a rank `n+2` dimensional input array.
    rhs: a rank `n+2` dimensional array of kernel weights.
    window_strides: a sequence of `n` integers, representing the inter-window
      strides.
    padding: either the string `'SAME'`, the string `'VALID'`.
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    An array containing the convolution result.
  """
  return conv_general_dilated(lhs, rhs, window_strides, padding,
                              precision=precision,
                              preferred_element_type=preferred_element_type)


def conv(
  scope,
  inputs,
  features,
  kernel_size,
  strides=None,
  padding='SAME',
  input_dilation=None,
  kernel_dilation=None,
  feature_group_count=1,
  bias=True,
  dtype=jnp.float32,
  precision=None,
  kernel_init=default_kernel_init,
  bias_init=initializers.zeros_init(),
):
  """Applies a convolution to the inputs.

  Args:
    inputs: input data with dimensions (batch, spatial_dims..., features).
    features: number of convolution filters.
    kernel_size: shape of the convolutional kernel.
    strides: a sequence of `n` integers, representing the inter-window
      strides.
    padding: either the string `'SAME'`, the string `'VALID'`, or a sequence
      of `n` `(low, high)` integer pairs that give the padding to apply before
      and after each spatial dimension.
    input_dilation: `None`, or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of `inputs`.
      Convolution with input dilation `d` is equivalent to transposed
      convolution with stride `d`.
    kernel_dilation: `None`, or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of the convolution
      kernel. Convolution with kernel dilation is also known as 'atrous
      convolution'.
    feature_group_count: integer, default 1. If specified divides the input
      features into groups.
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

  if strides is None:
    strides = (1,) * (inputs.ndim - 2)

  in_features = inputs.shape[-1]
  assert in_features % feature_group_count == 0
  kernel_shape = kernel_size + (in_features // feature_group_count, features)
  kernel = scope.param('kernel', kernel_init, kernel_shape)
  kernel = jnp.asarray(kernel, dtype)

  dimension_numbers = _conv_dimension_numbers(inputs.shape)
  y = lax.conv_general_dilated(
    inputs,
    kernel,
    strides,
    padding,
    lhs_dilation=input_dilation,
    rhs_dilation=kernel_dilation,
    dimension_numbers=dimension_numbers,
    feature_group_count=feature_group_count,
    precision=precision,
  )

  if bias:
    bias = scope.param('bias', bias_init, (features,))
    bias = jnp.asarray(bias, dtype)
    y += jnp.reshape(bias, (1,) * (y.ndim - 1) + (-1,))
  return y

