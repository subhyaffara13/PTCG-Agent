
def relu(x):
    return np.maximum(0, x)


def relu(input: Tensor, inplace: bool = False) -> Tensor:  # noqa: D400,D402
    r"""relu(input, inplace=False) -> Tensor

    Applies the rectified linear unit function element-wise. See
    :class:`~torch.nn.ReLU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(relu, (input,), input, inplace=inplace)
    if inplace:
        result = torch.relu_(input)
    else:
        result = torch.relu(input)
    return result


def relu(a: TensorLikeType, inplace: bool = False) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.relu
    """

    if inplace:
        raise NotImplementedError

    return torch.where(torch.le(a, 0), 0, a)


def relu(g: jit_utils.GraphContext, input):
    return symbolic_helper._op_with_optional_float_cast(
        g, "Relu", input, opset_before=14
    )


def relu(v: chex.Array) -> chex.Array:
  """Returns the element-wise maximum between `v` and 0."""
  return nn.relu(v)


def relu(v: np.ndarray) -> np.ndarray:
  """Returns the element-wise maximum between `v` and 0."""
  return np.maximum(v, 0)


def relu(x: ArrayLike) -> Array:
  r"""Rectified linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{relu}(x) = \max(x, 0)

  except under differentiation, we take:

  .. math::
    \nabla \mathrm{relu}(0) = 0

  For more information see
  `Numerical influence of ReLU’(0) on backpropagation
  <https://dl.acm.org/doi/10.5555/3540261.3540297>`_.

  Args:
    x : input array

  Returns:
    An array.

  Examples:
    >>> jax.nn.relu(jax.numpy.array([-2., -1., -0.5, 0, 0.5, 1., 2.]))
    Array([0. , 0. , 0. , 0. , 0.5, 1. , 2. ], dtype=float32)

  See also:
    :func:`relu6`

  """
  return jnp.maximum(x, 0)

