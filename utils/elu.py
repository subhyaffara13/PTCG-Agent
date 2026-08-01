
def elu(input: Tensor, alpha: float = 1.0, inplace: bool = False) -> Tensor:
    r"""Apply the Exponential Linear Unit (ELU) function element-wise.

    See :class:`~torch.nn.ELU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(elu, (input,), input, alpha=alpha, inplace=inplace)
    if inplace:
        result = torch._C._nn.elu_(input, alpha)
    else:
        result = torch._C._nn.elu(input, alpha)
    return result


def elu(
    a: TensorLikeType,
    alpha: NumberType = 1.0,
    scale: NumberType = 1.0,
    input_scale: NumberType = 1.0,
    inplace: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.elu
    """
    if inplace:
        raise NotImplementedError

    # nb. This should be factored out into a can_cast aux function
    python_type = utils.dtype_to_type(a.dtype)
    torch._check(
        utils.is_weakly_lesser_type(type(input_scale), python_type),
        lambda: f"input_scale argument of type {type(input_scale)} cannot be safely cast to type {python_type}!",
    )
    torch._check(
        utils.is_weakly_lesser_type(type(scale), python_type),
        lambda: f"scale argument of type {type(scale)} cannot be safely cast to type {python_type}!",
    )
    torch._check(
        utils.is_weakly_lesser_type(type(alpha), python_type),
        lambda: f"alpha argument of type {type(alpha)} cannot be safely cast to type {python_type}!",
    )

    return torch.where(a > 0, scale * a, (alpha * scale) * torch.expm1(a * input_scale))


def elu(g: jit_utils.GraphContext, input, alpha, scale, input_scale):
    if scale and scale != 1.0:
        return symbolic_helper._unimplemented(
            "scale", "does not support scale in Elu", scale
        )
    if input_scale and input_scale != 1.0:
        return symbolic_helper._unimplemented(
            "input_scale", "does not support input_scale in Elu", input_scale
        )
    # See Note [Export inplace]
    return g.op("Elu", input, alpha_f=symbolic_helper._scalar(alpha))


def elu(input: Tensor, scale: float, zero_point: int, alpha: float = 1.0) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.elu`.

    Args:
        input: quantized input
        scale: quantization scale of the output tensor
        zero_point: quantization zero point of the output tensor
        alpha: the alpha constant
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.elu' must be quantized!")
    return torch.ops.quantized.elu(input, scale, zero_point, alpha)


def elu(x: ArrayLike, alpha: ArrayLike = 1.0) -> Array:
  r"""Exponential linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{elu}(x) = \begin{cases}
      x, & x > 0\\
      \alpha \left(\exp(x) - 1\right), & x \le 0
    \end{cases}

  Args:
    x : input array
    alpha : scalar or array of alpha values (default: 1.0)

  Returns:
    An array.

  See also:
    :func:`selu`
  """
  x_arr = numpy_util.ensure_arraylike("elu", x)
  return jnp.where(x_arr > 0,
                   x_arr,
                   alpha * jnp.expm1(jnp.where(x_arr > 0, 0., x_arr)))

