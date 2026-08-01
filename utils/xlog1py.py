
def xlog1py(a: TensorLikeType | NumberType, b: TensorLikeType | NumberType):
    torch._check(
        isinstance(a, TensorLike) or isinstance(b, TensorLike),
        lambda: 'Expected either argument a or b to be a Tensor"',
    )

    # Operations like eq and log do not handle scalar values, so we convert them to scalar_tensors.
    if isinstance(a, TensorLike) and isinstance(b, Number):
        # pyrefly: ignore [bad-argument-type]
        b = refs.scalar_tensor(b, dtype=a.dtype, device=a.device)
    elif isinstance(b, TensorLike) and isinstance(a, Number):
        # pyrefly: ignore [bad-argument-type]
        a = refs.scalar_tensor(a, dtype=b.dtype, device=b.device)

    # mypy: expected "Tensor"
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if not isinstance(b, TensorLike):
        raise AssertionError(f"b must be TensorLike, got {type(b)}")
    rhs = torch.where(torch.eq(a, 0), 0, torch.mul(a, torch.log1p(b)))
    return torch.where(torch.isnan(b), float("nan"), rhs)


def xlog1py(x: ArrayLike, y: ArrayLike) -> Array:
  """Compute x*log(1 + y), returning 0 for x=0.

  JAX implementation of :obj:`scipy.special.xlog1py`.

  This is defined to return 0 when :math:`(x, y) = (0, -1)`, with a custom
  derivative rule so that automatic differentiation is well-defined at this point.

  Args:
    x: arraylike, real-valued.
    y: arraylike, real-valued.

  Returns:
    array containing xlog1py values.

  See also:
    :func:`jax.scipy.special.xlogy`
  """
  # Note: xlog1py(0, -1) should return 0 according to the function documentation.
  # NaN in y is propagated even when x == 0, to match scipy.special.xlog1py.
  x, y = promote_args_inexact("xlog1py", x, y)
  x_ok = x != 0.
  return jnp.where(x_ok | jnp.isnan(y), lax.mul(x, lax.log1p(y)), jnp.zeros_like(x))

