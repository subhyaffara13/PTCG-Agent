
def digamma(a):
    return prims.digamma(a)


def digamma(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DigammaOp(operand=operand, results=results, loc=loc, ip=ip).result


def digamma(x): return scipy.special.digamma(x).astype(x.dtype)


def digamma(x: ArrayLike) -> Array:
  r"""Elementwise digamma: :math:`\psi(x)`."""
  return digamma_p.bind(x)


def digamma(x: ArrayLike) -> Array:
  r"""The digamma function

  JAX implementation of :obj:`scipy.special.digamma`.

  .. math::

     \mathrm{digamma}(z) = \psi(z) = \frac{\mathrm{d}}{\mathrm{d}z}\log \Gamma(z)

  where :math:`\Gamma(z)` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the digamma function.

  Notes:
    The JAX version of `digamma` accepts real-valued inputs.

  See also:
    - :func:`jax.scipy.special.gamma`
    - :func:`jax.scipy.special.polygamma`
  """
  x, = promote_args_inexact("digamma", x)
  return lax.digamma(x)

