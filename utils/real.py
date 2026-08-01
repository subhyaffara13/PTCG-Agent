
def real(a: ArrayLike):
    return torch.real(a)


def real(a: TensorLikeType) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if utils.is_complex_dtype(a.dtype):
        return prims.real(a)
    return a


def real(val):
    """
    Return the real part of the complex argument.

    Parameters
    ----------
    val : array_like
        Input array.

    Returns
    -------
    out : ndarray or scalar
        The real component of the complex argument. If `val` is real, the type
        of `val` is used for the output.  If `val` has complex elements, the
        returned type is float.

    See Also
    --------
    real_if_close, imag, angle

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1+2j, 3+4j, 5+6j])
    >>> a.real
    array([1.,  3.,  5.])
    >>> a.real = 9
    >>> a
    array([9.+2.j,  9.+4.j,  9.+6.j])
    >>> a.real = np.array([9, 8, 7])
    >>> a
    array([9.+2.j,  8.+4.j,  7.+6.j])
    >>> np.real(1 + 1j)
    1.0

    """
    try:
        return val.real
    except AttributeError:
        return asanyarray(val).real


def real(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RealOp(operand=operand, results=results, loc=loc, ip=ip).result


def real(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RealOp(operand=operand, results=results, loc=loc, ip=ip).result


def real(x: ArrayLike) -> Array:
  r"""Elementwise extract real part: :math:`\mathrm{Re}(x)`.

  This function lowers directly to the `stablehlo.real`_ operation.

  Args:
    x: input array. Must have complex dtype.

  Returns:
    Array of the same shape as ``x`` containing its real part. Will have dtype
    float32 if ``x.dtype == complex64``, or float64 if ``x.dtype == complex128``.

  See also:
    - :func:`jax.lax.complex`: elementwise construct complex number.
    - :func:`jax.lax.imag`: elementwise extract imaginary part.
    - :func:`jax.lax.conj`: elementwise complex conjugate.

  .. _stablehlo.real: https://openxla.org/stablehlo/spec#real
  """
  return real_p.bind(x)


def real(val: ArrayLike, /) -> Array:
  """Return element-wise real part of the complex argument.

  JAX implementation of :obj:`numpy.real`.

  Args:
    val: input array or scalar.

  Returns:
    An array containing the real part of the elements of ``val``.

  See also:
    - :func:`jax.numpy.conjugate` and :func:`jax.numpy.conj`: Returns the element-wise
      complex-conjugate of the input.
    - :func:`jax.numpy.imag`: Returns the element-wise imaginary part of the
      complex argument.

  Examples:
    >>> jnp.real(5)
    Array(5, dtype=int32, weak_type=True)
    >>> jnp.real(2j)
    Array(0., dtype=float32, weak_type=True)
    >>> x = jnp.array([3-2j, 4+7j, -2j])
    >>> jnp.real(x)
    Array([ 3.,  4., -0.], dtype=float32)
  """
  val = ensure_arraylike("real", val)
  return lax.real(val) if np.iscomplexobj(val) else lax.asarray(val)

