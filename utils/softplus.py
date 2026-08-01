
def softplus(
    a: TensorLikeType,
    beta: NumberType | None = None,
    threshold: NumberType = 20,
    inplace: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.softplus
    """

    if inplace:
        raise NotImplementedError

    rhs: TensorLikeType
    if beta is not None:
        python_type = utils.dtype_to_type(a.dtype)
        if not utils.is_weakly_lesser_type(type(beta), python_type):
            msg = f"beta argument of type {type(beta)} cannot be safely cast to type {python_type}!"
            raise ValueError(msg)
        scaled_input = a * beta
        rhs = torch.true_divide(torch.log1p(torch.exp(scaled_input)), beta)  # type: ignore[arg-type]

    else:
        scaled_input = a
        rhs = torch.log1p(torch.exp(scaled_input))

    return torch.where(scaled_input > threshold, a, rhs)


def softplus(g: jit_utils.GraphContext, self, beta, threshold):
    beta_const = symbolic_helper._maybe_get_const(beta, "f")
    if beta_const != 1:
        return g.op("Div", g.op("Softplus", g.op("Mul", self, beta)), beta)
    return g.op("Softplus", self)


def softplus(x, **kwargs):
    r"""
    Compute the softplus function element-wise.

    The softplus function is defined as: ``softplus(x) = log(1 + exp(x))``.
    It is a smooth approximation of the rectifier function (ReLU).

    Parameters
    ----------
    x : array_like
        Input value.
    **kwargs
        For other keyword-only arguments, see the
        `ufunc docs <https://numpy.org/doc/stable/reference/ufuncs.html>`_.

    Returns
    -------
    softplus : ndarray
        Logarithm of ``exp(0) + exp(x)``.

    Examples
    --------
    >>> from scipy import special

    >>> special.softplus(0)
    0.6931471805599453

    >>> special.softplus([-1, 0, 1])
    array([0.31326169, 0.69314718, 1.31326169])
    """
    return np.logaddexp(0, x, **kwargs)


def softplus(x: ArrayLike) -> Array:
  r"""Softplus activation function.

  Computes the element-wise function

  .. math::
    \mathrm{softplus}(x) = \log(1 + e^x)

  Args:
    x : input array
  """
  return jnp.logaddexp(x, 0)

