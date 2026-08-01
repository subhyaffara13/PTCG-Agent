
def entr(a: TensorLikeType) -> TensorLikeType:
    return torch.where(
        torch.isnan(a),
        a,
        torch.where(a > 0, -a * torch.log(a), torch.where(a == 0, 0, -torch.inf)),
    )


def entr(x: ArrayLike) -> Array:
  r"""The entropy function

  JAX implementation of :obj:`scipy.special.entr`.

  .. math::

     \mathrm{entr}(x) = \begin{cases}
       -x\log(x) & x > 0 \\
       0 & x = 0\\
       -\infty & \mathrm{otherwise}
     \end{cases}

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing entropy values.

  See also:
    - :func:`jax.scipy.special.kl_div`
    - :func:`jax.scipy.special.rel_entr`
  """
  x, = promote_args_inexact("entr", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("entr does not support complex-valued inputs.")
  return lax.select(lax.lt(x, _lax_const(x, 0)),
                    lax.full_like(x, -np.inf),
                    lax.neg(_xlogx(x)))

