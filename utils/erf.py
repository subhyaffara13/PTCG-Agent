
def erf(x):
    """
    erf of a real number.
    """
    x = float(x)
    if x != x:
        return x
    if x < 0.0:
        return -erf(-x)
    if x >= 1.0:
        if x >= 6.0:
            return 1.0
        return 1.0 - _erfc_mid(x)
    return _erf_taylor(x)


def erf(a):
    return prims.erf(a)


def erf(g: jit_utils.GraphContext, input):
    return g.op("Erf", input)


def erf(ctx, z):
    z = ctx.convert(z)
    if ctx._is_real_type(z):
        try:
            return ctx._erf(z)
        except NotImplementedError:
            pass
    if ctx._is_complex_type(z) and not z.imag:
        try:
            return type(z)(ctx._erf(z.real))
        except NotImplementedError:
            pass
    return ctx._erf_complex(z)


def erf(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ErfOp(operand=operand, results=results, loc=loc, ip=ip).result


def erf(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ErfOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def erf(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ErfOp(operand=operand, results=results, loc=loc, ip=ip).result


def erf(x): return scipy.special.erf(x).astype(x.dtype)


def erf(x: ArrayLike) -> Array:
  r"""Elementwise error function: :math:`\mathrm{erf}(x)`."""
  return erf_p.bind(x)


def erf(x: ArrayLike) -> Array:
  r"""The error function

  JAX implementation of :obj:`scipy.special.erf`.

  .. math::

     \mathrm{erf}(x) = \frac{2}{\sqrt\pi} \int_{0}^x e^{-t^2} \mathrm{d}t

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the error function.

  Notes:
     The JAX version only supports real-valued inputs.

  See also:
    - :func:`jax.scipy.special.erfc`
    - :func:`jax.scipy.special.erfcx`
    - :func:`jax.scipy.special.erfinv`
  """
  x, = promote_args_inexact("erf", x)
  return lax.erf(x)

