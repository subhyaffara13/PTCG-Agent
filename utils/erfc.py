
def erfc(x):
    """
    erfc of a real number.
    """
    x = float(x)
    if x != x:
        return x
    if x < 0.0:
        if x < -6.0:
            return 2.0
        return 2.0-erfc(-x)
    if x > 9.0:
        return _erfc_asymp(x)
    if x >= 1.0:
        return _erfc_mid(x)
    return 1.0 - _erf_taylor(x)


def erfc(a):
    return prims.erfc(a)


def erfc(ctx, z):
    z = ctx.convert(z)
    if ctx._is_real_type(z):
        try:
            return ctx._erfc(z)
        except NotImplementedError:
            pass
    if ctx._is_complex_type(z) and not z.imag:
        try:
            return type(z)(ctx._erfc(z.real))
        except NotImplementedError:
            pass
    return ctx._erfc_complex(z)


def erfc(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ErfcOp(operand=operand, results=results, loc=loc, ip=ip).result


def erfc(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ErfcOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def erfc(x): return scipy.special.erfc(x).astype(x.dtype)


def erfc(x: ArrayLike) -> Array:
  r"""Elementwise complementary error function:
    :math:`\mathrm{erfc}(x) = 1 - \mathrm{erf}(x)`."""
  return erfc_p.bind(x)


def erfc(x: ArrayLike) -> Array:
  r"""The complement of the error function

  JAX implementation of :obj:`scipy.special.erfc`.

  .. math::

     \mathrm{erfc}(x) = \frac{2}{\sqrt\pi} \int_{x}^\infty e^{-t^2} \mathrm{d}t

  This is the complement of the error function :func:`~jax.scipy.special.erf`,
  ``erfc(x) = 1 - erf(x)``.

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the complement of the error function.

  Notes:
     The JAX version only supports real-valued inputs.

  See also:
    - :func:`jax.scipy.special.erf`
    - :func:`jax.scipy.special.erfcx`
    - :func:`jax.scipy.special.erfinv`
  """
  x, = promote_args_inexact("erfc", x)
  return lax.erfc(x)

