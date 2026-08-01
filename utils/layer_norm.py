
def layer_norm(
    input: Tensor,
    normalized_shape: list[int],
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Layer Normalization for last certain number of dimensions.

    See :class:`~torch.nn.LayerNorm` for details.
    """
    if has_torch_function_variadic(input, weight, bias):
        return handle_torch_function(
            layer_norm,
            (input, weight, bias),
            input,
            normalized_shape,
            weight=weight,
            bias=bias,
            eps=eps,
        )
    return torch.layer_norm(
        input, normalized_shape, weight, bias, eps, torch.backends.cudnn.enabled
    )


def layer_norm(
    input: Tensor,
    normalized_shape: ShapeType,
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    eps: float = 1e-5,
) -> Tensor:
    """
    Reference implementation of :func:`torch.nn.functional.layer_norm`.
    """
    return torch.native_layer_norm(input, normalized_shape, weight, bias, eps)[0]


def layer_norm(
    g: jit_utils.GraphContext,
    input: _C.Value,
    normalized_shape: Sequence[int],
    weight: _C.Value,
    bias: _C.Value,
    eps: float,
    cudnn_enable: bool,
):
    # normalized_shape: input shape from an expected input of size
    # axis: The first normalization dimension.
    # layer_norm normalizes on the last D dimensions,
    # where D is the size of normalized_shape
    axis = -len(normalized_shape)
    scalar_type = _type_utils.JitScalarType.from_value(
        input, _type_utils.JitScalarType.FLOAT
    )
    dtype = scalar_type.dtype()
    if symbolic_helper._is_none(weight):
        weight_value = torch.ones(normalized_shape, dtype=dtype)
        weight = g.op("Constant", value_t=weight_value)
    if symbolic_helper._is_none(bias):
        bias_value = torch.zeros(normalized_shape, dtype=dtype)
        bias = g.op("Constant", value_t=bias_value)
    return g.op(
        "LayerNormalization",
        input,
        weight,
        bias,
        epsilon_f=eps,
        axis_i=axis,
    )


def layer_norm(
    g: jit_utils.GraphContext,
    input: _C.Value,
    normalized_shape: Sequence[int],
    weight: _C.Value,
    bias: _C.Value,
    eps: float,
    cudnn_enable: bool,
) -> _C.Value:
    normalized, _, _ = native_layer_norm(g, input, normalized_shape, weight, bias, eps)
    return normalized


def layer_norm(
    x, weight, bias,
    num_warps: int | None = None,
    num_stages: int | None = 3,
    eps: float = 1e-5,
    backward_pass_impl: str = 'triton',
    interpret: bool = False):
  n = x.shape[-1]
  # Triton heuristics
  # Less than 64KB per feature: enqueue fused kernel
  max_fused_size = 65536 // x.dtype.itemsize
  block_size = min(max_fused_size, pl.next_power_of_2(n))
  block_size = min(max(block_size, 128), 4096)
  num_warps = min(max(block_size // 256, 1), 8)

  kernel = functools.partial(layer_norm_forward_kernel, eps=eps,
                             block_size=block_size)
  out_shape = jax.ShapeDtypeStruct(shape=(n,), dtype=x.dtype)
  method = pl.pallas_call(
      kernel,
      compiler_params=plgpu.CompilerParams(
          num_warps=num_warps, num_stages=num_stages),
      grid=(),
      out_shape=out_shape,
      debug=False,
      interpret=interpret,
  )
  method = jax.vmap(jax.vmap(method, in_axes=(0, None, None)), in_axes=(0, None, None))
  return method(x, weight, bias)


def layer_norm(
  scope: Scope,
  x,
  epsilon=1e-6,
  dtype=jnp.float32,
  bias=True,
  scale=True,
  bias_init=initializers.zeros_init(),
  scale_init=initializers.ones_init(),
):
  """Applies layer normalization on the input.
  It normalizes the activations of the layer for each given example in a
  batch independently, rather than across a batch like Batch Normalization.
  i.e. applies a transformation that maintains the mean activation within
  each example close to 0 and the activation standard deviation close to 1.
  Args:
    x: the inputs
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
  features = x.shape[-1]
  mean = jnp.mean(x, axis=-1, keepdims=True)
  mean2 = jnp.mean(lax.square(x), axis=-1, keepdims=True)
  var = mean2 - lax.square(mean)
  mul = lax.rsqrt(var + epsilon)
  if scale:
    mul = mul * jnp.asarray(
      scope.param('scale', scale_init, (features,)), dtype
    )
  y = (x - mean) * mul
  if bias:
    y = y + jnp.asarray(scope.param('bias', bias_init, (features,)), dtype)
  return y

