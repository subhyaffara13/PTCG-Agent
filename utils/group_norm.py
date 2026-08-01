
def group_norm(
    input: Tensor,
    num_groups: int,
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Group Normalization for last certain number of dimensions.

    See :class:`~torch.nn.GroupNorm` for details.
    """
    if has_torch_function_variadic(input, weight, bias):
        return handle_torch_function(
            group_norm,
            (
                input,
                weight,
                bias,
            ),
            input,
            num_groups,
            weight=weight,
            bias=bias,
            eps=eps,
        )
    if input.dim() < 2:
        raise RuntimeError(
            f"Expected at least 2 dimensions for input tensor but received {input.dim()}"
        )
    _verify_batch_size(
        [input.size(0) * input.size(1) // num_groups, num_groups]
        + list(input.size()[2:])
    )
    return torch.group_norm(
        input, num_groups, weight, bias, eps, torch.backends.cudnn.enabled
    )


def group_norm(
    input: Tensor,
    num_groups: int,
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    eps: float = 1e-5,
) -> Tensor:
    """
    Reference implementation of :func:`torch.nn.functional.group_norm`.
    """
    torch._check(
        input.ndim >= 2,
        lambda: f"Expected at least 2 dimensions for input tensor but received {input.ndim}",
    )

    batch_size = input.shape[0]
    num_channels = input.shape[1]
    torch._check(
        num_channels % num_groups == 0,
        lambda: "Expected number of channels in input to be divisible by num_groups, "
        + f"but got input of shape {input.shape} and num_groups = {num_groups}",
    )

    # input shape is (N, C, *), so we flatten all inner dimensions except (N, C)
    flattened_inner_size = 1
    for dim_length in input.shape[2:]:
        flattened_inner_size *= dim_length

    return torch.native_group_norm(
        input,
        weight,
        bias,
        batch_size,
        num_channels,
        flattened_inner_size,
        num_groups,
        eps,
    )[0]


def group_norm(
    g: jit_utils.GraphContext, input, num_groups, weight, bias, eps, cudnn_enabled
):
    channel_size = symbolic_helper._get_tensor_dim_size(input, 1)
    if channel_size is not None:
        if channel_size % num_groups != 0:
            raise AssertionError(
                f"channel_size ({channel_size}) must be divisible by num_groups ({num_groups})"
            )
    input_rank = symbolic_helper._get_tensor_rank(input)
    if input_rank is None:
        return symbolic_helper._unimplemented("group_norm", "unknown input rank", input)
    # 0 in the shape list keeps dimension value unchanged.
    shape = [0, num_groups, -1]
    input_reshaped = symbolic_helper._reshape_helper(
        g, input, g.op("Constant", value_t=torch.LongTensor(shape))
    )

    # C is always divisible by num_groups
    # Due to shape difference. we need to apply weight and bias after
    # instance norm computation and reshape
    weight_ = g.op(
        "Constant",
        value_t=torch.tensor(
            [1.0] * num_groups,
            dtype=_type_utils.JitScalarType.from_value(input).dtype(),
        ),
    )
    bias_ = g.op(
        "Constant",
        value_t=torch.tensor(
            [0.0] * num_groups,
            dtype=_type_utils.JitScalarType.from_value(input).dtype(),
        ),
    )

    norm_reshaped = g.op(
        "InstanceNormalization", input_reshaped, weight_, bias_, epsilon_f=eps
    )
    norm = symbolic_helper._reshape_helper(g, norm_reshaped, g.op("Shape", input))

    if weight is None or weight.node().mustBeNone():
        weight_value = torch.tensor(
            [1.0], dtype=_type_utils.JitScalarType.from_value(input).dtype()
        )
        weight = g.op("Constant", value_t=weight_value)
    if bias is None or bias.node().mustBeNone():
        bias_value = torch.tensor(
            [0.0], dtype=_type_utils.JitScalarType.from_value(input).dtype()
        )
        bias = g.op("Constant", value_t=bias_value)

    # Norm has shape [N, C, *] so we reshape weight and bias to [C, *]
    axes = list(range(1, input_rank - 1))
    return add(
        g,
        mul(g, norm, symbolic_helper._unsqueeze_helper(g, weight, axes)),
        symbolic_helper._unsqueeze_helper(g, bias, axes),
    )


def group_norm(
  scope,
  x,
  num_groups=32,
  group_size=None,
  epsilon=1e-6,
  dtype=jnp.float32,
  bias=True,
  scale=True,
  bias_init=initializers.zeros_init(),
  scale_init=initializers.ones_init(),
):
  """Applies group normalization to the input (arxiv.org/abs/1803.08494).
  This op is similar to batch normalization, but statistics are shared across
  equally-sized groups of channels and not shared across batch dimension.
  Thus, group normalization does not depend on the batch composition and does
  not require maintaining internal state for storing statistics.
  The user should either specify the total number of channel groups or the
  number of channels per group.
  Args:
    x: the input of shape N...C, where N is a batch dimension and C is a
      channels dimensions. `...` represents an arbitrary number of extra
      dimensions that are used to accumulate statistics over.
    num_groups: the total number of channel groups. The default value of 32 is
      proposed by the original group normalization paper.
    group_size: the number of channels in a group.
    epsilon: A small float added to variance to avoid dividing by zero.
    dtype: the dtype of the computation (default: float32).
    bias:  If True, bias (beta) is added.
    scale: If True, multiply by scale (gamma). When the next layer is linear
      (also e.g. nn.relu), this can be disabled since the scaling will be done
      by the next layer.
    bias_init: Initializer for bias, by default, zero.
    scale_init: Initializer for scale, by default, one.
  Returns:
    Normalized inputs (the same shape as inputs).
  """
  x = jnp.asarray(x, jnp.float32)
  if (num_groups is None and group_size is None) or (
    num_groups is not None and group_size is not None
  ):
    raise ValueError(
      'Either `num_groups` or `group_size` should be '
      'specified, but not both of them.'
    )

  if group_size is not None:
    channels = x.shape[-1]
    if channels % group_size != 0:
      raise ValueError(
        'Number of channels ({}) is not multiple of the '
        'group size ({}).'.format(channels, group_size)
      )
    num_groups = channels // group_size

  input_shape = x.shape
  group_shape = x.shape[:-1] + (num_groups, x.shape[-1] // num_groups)

  x = x.reshape(group_shape)

  reduction_axis = list(range(1, x.ndim - 2)) + [x.ndim - 1]

  mean = jnp.mean(x, axis=reduction_axis, keepdims=True)
  mean_of_squares = jnp.mean(jnp.square(x), axis=reduction_axis, keepdims=True)
  var = mean_of_squares - jnp.square(mean)

  x = (x - mean) * lax.rsqrt(var + epsilon)

  x = x.reshape(input_shape)

  feature_shape = tuple([1 for d in input_shape[:-1]] + [input_shape[-1]])
  if scale:
    x = x * scope.param('scale', scale_init, feature_shape)
  if bias:
    x = x + scope.param('bias', bias_init, feature_shape)

  return x.astype(dtype)

