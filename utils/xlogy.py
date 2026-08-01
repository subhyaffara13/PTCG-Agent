
def xlogy(a: TensorLikeType | NumberType, b: TensorLikeType | NumberType):
    torch._check(
        isinstance(a, TensorLike) or isinstance(b, TensorLike),
        lambda: 'Expected either argument a or b to be a Tensor"',
    )

    # Operations like eq and log do not handle scalar values, so we convert them to scalar_tensors.
    if isinstance(b, TensorLike) and isinstance(a, Number):
        # pyrefly: ignore [bad-argument-type]
        a = scalar_tensor(a, dtype=b.dtype, device=b.device)
    elif isinstance(a, TensorLike) and isinstance(b, Number):
        # pyrefly: ignore [bad-argument-type]
        b = scalar_tensor(b, dtype=a.dtype, device=a.device)

    # mypy: expected "Tensor"
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if not isinstance(b, TensorLike):
        raise AssertionError(f"b must be TensorLike, got {type(b)}")
    rhs = torch.where(torch.eq(a, 0), 0, torch.mul(a, torch.log(b)))
    return torch.where(torch.isnan(b), float("nan"), rhs)


def xlogy(x: ArrayLike, y: ArrayLike) -> Array:
  """Compute x*log(y), returning 0 for x=0.

  JAX implementation of :obj:`scipy.special.xlogy`.

  This is defined to return zero when :math:`(x, y) = (0, 0)`, with a custom
  derivative rule so that automatic differentiation is well-defined at this point.

  Args:
    x: arraylike, real-valued.
    y: arraylike, real-valued.

  Returns:
    array containing xlogy values.

  See also:
    :func:`jax.scipy.special.xlog1py`
  """
  # Note: xlogy(0, 0) should return 0 according to the function documentation.
  # NaN in y is propagated even when x == 0, to match scipy.special.xlogy.
  x, y = promote_args_inexact("xlogy", x, y)
  x_ok = x != 0.
  return jnp.where(x_ok | jnp.isnan(y), lax.mul(x, lax.log(y)), jnp.zeros_like(x))

