
def relu6(input: Tensor, inplace: bool = False) -> Tensor:  # noqa: D400,D402
    r"""relu6(input, inplace=False) -> Tensor

    Applies the element-wise function :math:`\text{ReLU6}(x) = \min(\max(0,x), 6)`.

    See :class:`~torch.nn.ReLU6` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(relu6, (input,), input, inplace=inplace)
    if inplace:
        result = torch._C._nn.relu6_(input)
    else:
        result = torch._C._nn.relu6(input)
    return result


def relu6(a: TensorLikeType, inplace: bool = False) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.relu6
    """
    if inplace:
        raise NotImplementedError

    # See https://github.com/pytorch/pytorch/pull/81142#discussion_r918220126
    # It may be better to use clamp here, but we use hardtanh to replicate
    # the behavior of the existing implementation
    return torch.nn.functional.hardtanh(a, 0, 6)


def relu6(g: jit_utils.GraphContext, input):
    scalar_type = _type_utils.JitScalarType.from_value(
        input, _type_utils.JitScalarType.FLOAT
    )
    min_val = g.op(
        "Constant",
        value_t=torch.tensor(0, dtype=scalar_type.dtype()),
    )
    max_val = g.op(
        "Constant",
        value_t=torch.tensor(6, dtype=scalar_type.dtype()),
    )
    return clamp(g, input, min_val, max_val)


def relu6(g: jit_utils.GraphContext, input):
    return clamp(g, input, 0, 6)


def relu6(x: ArrayLike) -> Array:
  r"""Rectified Linear Unit 6 activation function.

  Computes the element-wise function

  .. math::
    \mathrm{relu6}(x) = \min(\max(x, 0), 6)

  except under differentiation, we take:

  .. math::
    \nabla \mathrm{relu}(0) = 0

  and

  .. math::
    \nabla \mathrm{relu}(6) = 0

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`relu`
  """
  return jnp.minimum(jnp.maximum(x, 0), 6.)

