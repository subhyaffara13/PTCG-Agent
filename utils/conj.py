
def conj(input: TensorLikeType) -> TensorLikeType:
    if not utils.is_complex_dtype(input.dtype):
        return input
    if input.is_sparse:
        return torch.conj_physical(input)
    return prims.conj(input)


def conj(ctx, x):
    x = ctx.convert(x)
    try:
        return x.conjugate()
    except AttributeError:
        return x


def conj(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConjOp(operand=operand, results=results, loc=loc, ip=ip).result


def conj(x):
  return np.conj(x) + np.complex64(0)


def conj(x: ArrayLike) -> Array:
  r"""Elementwise complex conjugate function: :math:`\overline{x}`.

  This function lowers to a combination of `stablehlo.real`_, `stablehlo.imag`_,
  and  `stablehlo.complex`_.

  Args:
    x: input array. Must have complex dtype.

  Returns:
    Array of the same shape and dtype as ``x`` containing its complex conjugate.

  See also:
    - :func:`jax.lax.complex`: elementwise construct complex number.
    - :func:`jax.lax.real`: elementwise extract real part.
    - :func:`jax.lax.imag`: elementwise extract imaginary part.
    - :func:`jax.lax.abs`: elementwise absolute value / complex magnitude.

  .. _stablehlo.real: https://openxla.org/stablehlo/spec#real
  .. _stablehlo.imag: https://openxla.org/stablehlo/spec#imag
  .. _stablehlo.complex: https://openxla.org/stablehlo/spec#complex
  """
  # TODO(mattjj): remove input_dtype, not needed anymore
  return conj_p.bind(x, input_dtype=_dtype(x))


def conj(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.conjugate`"""
  return conjugate(x)

