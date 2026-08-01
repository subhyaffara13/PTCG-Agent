
def mish(input: Tensor, inplace: bool = False) -> Tensor:
    r"""Apply the Mish function, element-wise.

    Mish: A Self Regularized Non-Monotonic Neural Activation Function.

    .. math::
        \text{Mish}(x) = x * \text{Tanh}(\text{Softplus}(x))

    .. note::
        See `Mish: A Self Regularized Non-Monotonic Neural Activation Function <https://arxiv.org/abs/1908.08681>`_

    See :class:`~torch.nn.Mish` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(mish, (input,), input, inplace=inplace)
    if inplace:
        return torch._C._nn.mish_(input)
    return torch._C._nn.mish(input)


def mish(a: TensorLikeType, inplace: bool = False) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.mish
    """

    if inplace:
        raise NotImplementedError
    return a * torch.tanh(torch.nn.functional.softplus(a))


def mish(g: jit_utils.GraphContext, input):
    return g.op("Mul", input, g.op("Tanh", g.op("Softplus", input)))


def mish(x: ArrayLike) -> Array:
  r"""Mish activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{mish}(x) = x \cdot \mathrm{tanh}(\mathrm{softplus}(x))

  For more information, see
  `Mish: A Self Regularized Non-Monotonic Activation Function
  <https://arxiv.org/abs/1908.08681>`_.

  Args:
    x : input array

  Returns:
    An array.
  """
  x_arr = numpy_util.ensure_arraylike("mish", x)
  return x_arr * jnp.tanh(softplus(x_arr))

