
def sigmoid(self: Tensor) -> Tensor:
    _, result_dtype = elementwise_dtypes(
        self,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )
    return torch.empty_like(self, dtype=result_dtype)


def sigmoid(_outputs):
    return 1.0 / (1.0 + np.exp(-_outputs))


def sigmoid(_outputs):
    return 1.0 / (1.0 + np.exp(-_outputs))


def sigmoid(input):  # noqa: D400,D402
    r"""sigmoid(input) -> Tensor

    Applies the element-wise function :math:`\text{Sigmoid}(x) = \frac{1}{1 + \exp(-x)}`

    See :class:`~torch.nn.Sigmoid` for more details.
    """
    return input.sigmoid()


def sigmoid(a: TensorLikeType) -> TensorLikeType:
    return true_divide(1, add(1, exp(neg(a))))


def sigmoid(g: jit_utils.GraphContext, self):
    """Converts the corresponding PyTorch function into ONNX operators.

    It is not meant to be called directly by a user.

    Args:
        g (jit_utils.GraphContext): Graph context.
        self (Tensor): the input tensor.
    Returns:
        ONNX operator
    """
    return g.op("Sigmoid", self)


def sigmoid(ctx, t, amplitude=1):
    A = amplitude
    return A / (1 + ctx.exp(-t))


def sigmoid(x: ArrayLike) -> Array:
  r"""Sigmoid activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{sigmoid}(x) = \frac{1}{1 + e^{-x}}

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`log_sigmoid`

  """
  return lax.logistic(x)

