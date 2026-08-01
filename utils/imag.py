
def imag(a: ArrayLike):
    if a.is_complex():
        return a.imag
    return torch.zeros_like(a)


def imag(a: TensorLikeType) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    torch._check(
        utils.is_complex_dtype(a.dtype), lambda: "imag only supports complex tensors."
    )
    return prims.imag(a)


def imag(val):
    """
    Return the imaginary part of the complex argument.

    Parameters
    ----------
    val : array_like
        Input array.

    Returns
    -------
    out : ndarray or scalar
        The imaginary component of the complex argument. If `val` is real,
        the type of `val` is used for the output.  If `val` has complex
        elements, the returned type is float.

    See Also
    --------
    real, angle, real_if_close

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1+2j, 3+4j, 5+6j])
    >>> a.imag
    array([2.,  4.,  6.])
    >>> a.imag = np.array([8, 10, 12])
    >>> a
    array([1. +8.j,  3.+10.j,  5.+12.j])
    >>> np.imag(1 + 1j)
    1.0

    """
    try:
        return val.imag
    except AttributeError:
        return asanyarray(val).imag


def imag(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ImagOp(operand=operand, results=results, loc=loc, ip=ip).result


def imag(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ImagOp(operand=operand, results=results, loc=loc, ip=ip).result


def imag(x: ArrayLike) -> Array:
  r"""Elementwise extract imaginary part: :math:`\mathrm{Im}(x)`.

  This function lowers directly to the `stablehlo.imag`_ operation.

  Args:
    x: input array. Must have complex dtype.

  Returns:
    Array of the same shape as ``x`` containing its imaginary part. Will have dtype
    float32 if ``x.dtype == complex64``, or float64 if ``x.dtype == complex128``.

  See also:
    - :func:`jax.lax.complex`: elementwise construct complex number.
    - :func:`jax.lax.real`: elementwise extract real part.
    - :func:`jax.lax.conj`: elementwise complex conjugate.

  .. _stablehlo.imag: https://openxla.org/stablehlo/spec#imag
  """
  return imag_p.bind(x)


def imag(val: ArrayLike, /) -> Array:
  """Return element-wise imaginary of part of the complex argument.

  JAX implementation of :obj:`numpy.imag`.

  Args:
    val: input array or scalar.

  Returns:
    An array containing the imaginary part of the elements of ``val``.

  See also:
    - :func:`jax.numpy.conjugate` and :func:`jax.numpy.conj`: Returns the element-wise
      complex-conjugate of the input.
    - :func:`jax.numpy.real`: Returns the element-wise real part of the complex
      argument.

  Examples:
    >>> jnp.imag(4)
    Array(0, dtype=int32, weak_type=True)
    >>> jnp.imag(5j)
    Array(5., dtype=float32, weak_type=True)
    >>> x = jnp.array([2+3j, 5-1j, -3])
    >>> jnp.imag(x)
    Array([ 3., -1.,  0.], dtype=float32)
  """
  val = ensure_arraylike("imag", val)
  return lax.imag(val) if np.iscomplexobj(val) else lax.full_like(val, 0)

