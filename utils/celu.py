
def celu(
    input: Tensor,
    alpha: float = 1.0,
    inplace: bool = False,
) -> Tensor:  # noqa: D400,D402
    r"""celu(input, alpha=1., inplace=False) -> Tensor

    Applies element-wise,
    :math:`\text{CELU}(x) = \max(0,x) + \min(0, \alpha * (\exp(x/\alpha) - 1))`.

    See :class:`~torch.nn.CELU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            celu, (input,), input, alpha=alpha, inplace=inplace
        )
    if inplace:
        result = torch.celu_(input, alpha)
    else:
        result = torch.celu(input, alpha)
    return result


def celu(
    a: TensorLikeType, alpha: NumberType | None = None, inplace: bool = False
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.celu
    """

    if inplace:
        raise NotImplementedError

    rhs: TensorLikeType
    if alpha is not None:
        python_type = utils.dtype_to_type(a.dtype)
        if not utils.is_weakly_lesser_type(type(alpha), python_type):
            msg = f"alpha argument of type {type(alpha)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        rhs = alpha * torch.expm1(torch.true_divide(a, alpha))  # type: ignore[arg-type]
    else:
        rhs = torch.expm1(a)

    return torch.where(a > 0, a, rhs)


def celu(g: jit_utils.GraphContext, self, alpha):
    alpha = symbolic_helper._maybe_get_const(alpha, "f")
    # if the input is of type double cast it to float
    if (
        _type_utils.JitScalarType.from_value(self, _type_utils.JitScalarType.UNDEFINED)
        == _type_utils.JitScalarType.DOUBLE
    ):
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)
        out = g.op("Celu", self, alpha_f=alpha)
        return g.op("Cast", out, to_i=_C_onnx.TensorProtoDataType.DOUBLE)

    return g.op("Celu", self, alpha_f=alpha)


def celu(input: Tensor, scale: float, zero_point: int, alpha: float = 1.0) -> Tensor:
    r"""celu(input, scale, zero_point, alpha=1.) -> Tensor

    Applies the quantized CELU function element-wise.

    .. math::
        \text{CELU}(x) = \max(0,x) + \min(0, \alpha * (\exp(x / \alpha) - 1))

    Args:
        input: quantized input
        alpha: the :math:`\alpha` value for the CELU formulation. Default: 1.0
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.celu' must be quantized!")
    return torch.ops.quantized.celu(input, scale, zero_point, alpha)


def celu(x: ArrayLike, alpha: ArrayLike = 1.0) -> Array:
  r"""Continuously-differentiable exponential linear unit activation.

  Computes the element-wise function:

  .. math::
    \mathrm{celu}(x) = \begin{cases}
      x, & x > 0\\
      \alpha \left(\exp(\frac{x}{\alpha}) - 1\right), & x \le 0
    \end{cases}

  For more information, see
  `Continuously Differentiable Exponential Linear Units
  <https://arxiv.org/abs/1704.07483>`_.

  Args:
    x : input array
    alpha : array or scalar (default: 1.0)

  Returns:
    An array.
  """
  return jnp.maximum(x, 0.0) + alpha * jnp.expm1(jnp.minimum(x, 0.0) / alpha)

