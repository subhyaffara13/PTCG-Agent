
def batch_norm(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
    training: bool,
    momentum: float,
    eps: float,
    cudnn_enabled: bool,
):
    out: list[int] = []
    for elem in input:
        out.append(elem)
    return out


def batch_norm(
    input: Tensor,
    running_mean: Tensor | None,
    running_var: Tensor | None,
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    training: bool = False,
    momentum: float = 0.1,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Batch Normalization for each channel across a batch of data.

    See :class:`~torch.nn.BatchNorm1d`, :class:`~torch.nn.BatchNorm2d`,
    :class:`~torch.nn.BatchNorm3d` for details.
    """
    if has_torch_function_variadic(input, running_mean, running_var, weight, bias):
        return handle_torch_function(
            batch_norm,
            (input, running_mean, running_var, weight, bias),
            input,
            running_mean,
            running_var,
            weight=weight,
            bias=bias,
            training=training,
            momentum=momentum,
            eps=eps,
        )
    if training:
        # pyrefly: ignore [bad-argument-type]
        _verify_batch_size(input.size())

    if training and eps <= 0.0:
        raise ValueError(
            f"batch_norm eps must be positive during training, but got {eps}"
        )
    elif eps < 0.0:
        raise ValueError(f"batch_norm eps must be non-negative, but got {eps}")

    return torch.batch_norm(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        training,
        momentum,
        eps,
        torch.backends.cudnn.enabled,
    )


def batch_norm(
    g: jit_utils.GraphContext,
    input,
    weight,
    bias,
    running_mean,
    running_var,
    training,
    momentum,
    eps,
    cudnn_enabled,
):
    if (
        torch.is_autocast_enabled()
        and not symbolic_helper.args_have_same_dtype(
            [input, weight, bias, running_mean, running_var]
        )
        and GLOBALS.export_onnx_opset_version < 15
    ):
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "BatchNormalization",
            14,
            15,
            "All input tensors must have the same `dtype`."
            " Turn off Autocast or export using opset version 15.",
            input,
        )

    symbolic_helper.check_training_mode(training, "batch_norm")
    weight, bias, running_mean, running_var = symbolic_helper._batchnorm_helper(
        g, input, weight, bias, running_mean, running_var
    )
    out = g.op(
        "BatchNormalization",
        input,
        weight,
        bias,
        running_mean,
        running_var,
        epsilon_f=eps,
        momentum_f=1 - momentum,
        training_mode_i=0 if not training else 1,
        outputs=1 if not training else 3,
    )
    if not training:
        return out
    else:
        res, new_running_mean, new_running_var = out
        new_running_mean.setType(running_mean.type())
        new_running_var.setType(running_var.type())
        return res


def batch_norm(
    g: jit_utils.GraphContext,
    input,
    weight,
    bias,
    running_mean,
    running_var,
    training,
    momentum,
    eps,
    cudnn_enabled,
):
    symbolic_helper.check_training_mode(training, "batch_norm")

    if (
        torch.is_autocast_enabled()
        and not symbolic_helper.args_have_same_dtype(
            [input, weight, bias, running_mean, running_var]
        )
        and GLOBALS.export_onnx_opset_version < 15
    ):
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "BatchNormalization",
            9,
            15,
            "All input tensors must have the same `dtype`."
            " Turn off Autocast or export using opset version 15.",
            input,
        )

    weight, bias, running_mean, running_var = symbolic_helper._batchnorm_helper(
        g, input, weight, bias, running_mean, running_var
    )
    out = g.op(
        "BatchNormalization",
        input,
        weight,
        bias,
        running_mean,
        running_var,
        epsilon_f=eps,
        momentum_f=1 - momentum,
        outputs=1 if not training else 5,
    )
    if not training:
        return out
    else:
        res, new_running_mean, new_running_var, saved_mean, saved_var = out
        new_running_mean.setType(running_mean.type())
        new_running_var.setType(running_var.type())
        saved_mean.setDebugName("batch_norm_dead_output-" + saved_mean.debugName())
        saved_var.setDebugName("batch_norm_dead_output-" + saved_var.debugName())
        return res


def BatchNorm(axis=(0, 1, 2), epsilon=1e-5, center=True, scale=True,
              beta_init=zeros, gamma_init=ones):
  """Layer construction function for a batch normalization layer."""
  _beta_init = lambda rng, shape: beta_init(rng, shape) if center else ()
  _gamma_init = lambda rng, shape: gamma_init(rng, shape) if scale else ()
  axis = (axis,) if jnp.isscalar(axis) else axis
  def init_fun(rng, input_shape):
    shape = tuple(d for i, d in enumerate(input_shape) if i not in axis)
    k1, k2 = random.split(rng)
    beta, gamma = _beta_init(k1, shape), _gamma_init(k2, shape)
    return input_shape, (beta, gamma)
  def apply_fun(params, x, **kwargs):
    beta, gamma = params
    # TODO(phawkins): jnp.expand_dims should accept an axis tuple.
    # (https://github.com/numpy/numpy/issues/12290)
    ed = tuple(None if i in axis else slice(None) for i in range(jnp.ndim(x)))
    z = standardize(x, axis, epsilon=epsilon)
    if center and scale: return gamma[ed] * z + beta[ed]
    if center: return z + beta[ed]
    if scale: return gamma[ed] * z
    return z
  return init_fun, apply_fun


def batch_norm(
  scope: Scope,
  x,
  use_running_average=False,
  axis=-1,
  momentum=0.99,
  epsilon=1e-5,
  dtype=jnp.float32,
  bias=True,
  scale=True,
  bias_init=initializers.zeros_init(),
  scale_init=initializers.ones_init(),
  axis_name=None,
  axis_index_groups=None,
  kind='batch_stats',
):
  x = jnp.asarray(x, jnp.float32)
  axis = axis if isinstance(axis, tuple) else (axis,)
  axis = _absolute_dims(x.ndim, axis)
  redux = tuple(i for i in range(x.ndim) if i not in axis)

  def pmean(x):
    m = jnp.mean(x, redux, keepdims=True)
    if axis_name is not None:
      m = lax.pmean(m, axis_name=axis_name, axis_index_groups=axis_index_groups)
    return m

  mean = pmean(x)
  squeeze_shape = jnp.squeeze(mean).shape
  mean2 = pmean(jnp.square(x))
  var = mean2 - jnp.square(mean)

  is_init = not scope.has_variable(kind, 'mean')
  ra_mean = scope.variable(kind, 'mean', jnp.zeros, squeeze_shape)
  ra_var = scope.variable(kind, 'var', jnp.ones, squeeze_shape)

  if use_running_average:
    # if ra_mean is not None:
    #   raise ValueError('batch_stats should be provided if use_running_averages=True')
    mean = jnp.reshape(ra_mean.value, mean.shape)
    var = jnp.reshape(ra_var.value, var.shape)
  else:
    if not is_init:
      beta = 1.0 - momentum
      ra_mean.value += beta * (jnp.squeeze(mean) - ra_mean.value)
      ra_var.value += beta * (jnp.squeeze(var) - ra_var.value)
  y = x - mean
  mul = lax.rsqrt(var + epsilon)
  if scale:
    mul = mul * scope.param('scale', scale_init, squeeze_shape).reshape(
      mean.shape
    )
  y = y * mul
  if bias:
    y = y + scope.param('bias', bias_init, squeeze_shape).reshape(mean.shape)
  return jnp.asarray(y, dtype)

