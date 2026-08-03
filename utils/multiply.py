import sys

def multiply(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """
    Superimposes two images on top of each other.

    If you multiply an image with a solid black image, the result is black. If
    you multiply with a solid white image, the image is unaffected. ::

        out = image1 * image2 / MAX

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_multiply(image2.im))


def multiply(a, i):
    """
    Return (a * i), that is string multiple concatenation,
    element-wise.

    Values in ``i`` of less than 0 are treated as 0 (which yields an
    empty string).

    Parameters
    ----------
    a : array_like, with ``bytes_`` or ``str_`` dtype

    i : array_like, with any integer dtype

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input types

    Notes
    -----
    This is a thin wrapper around np.strings.multiply that raises
    `ValueError` when ``i`` is not an integer. It only
    exists for backwards-compatibility.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["a", "b", "c"])
    >>> np.strings.multiply(a, 3)
    array(['aaa', 'bbb', 'ccc'], dtype='<U3')
    >>> i = np.array([1, 2, 3])
    >>> np.strings.multiply(a, i)
    array(['a', 'bb', 'ccc'], dtype='<U3')
    >>> np.strings.multiply(np.array(['a']), i)
    array(['a', 'aa', 'aaa'], dtype='<U3')
    >>> a = np.array(['a', 'b', 'c', 'd', 'e', 'f']).reshape((2, 3))
    >>> np.strings.multiply(a, 3)
    array([['aaa', 'bbb', 'ccc'],
           ['ddd', 'eee', 'fff']], dtype='<U3')
    >>> np.strings.multiply(a, i)
    array([['a', 'bb', 'ccc'],
           ['d', 'ee', 'fff']], dtype='<U3')

    """
    try:
        return strings_multiply(a, i)
    except TypeError:
        raise ValueError("Can only multiply by integers")


def multiply(a, i):
    """
    Return (a * i), that is string multiple concatenation,
    element-wise.

    Values in ``i`` of less than 0 are treated as 0 (which yields an
    empty string).

    Parameters
    ----------
    a : array_like, with ``StringDType``, ``bytes_`` or ``str_`` dtype

    i : array_like, with any integer dtype

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["a", "b", "c"])
    >>> np.strings.multiply(a, 3)
    array(['aaa', 'bbb', 'ccc'], dtype='<U3')
    >>> i = np.array([1, 2, 3])
    >>> np.strings.multiply(a, i)
    array(['a', 'bb', 'ccc'], dtype='<U3')
    >>> np.strings.multiply(np.array(['a']), i)
    array(['a', 'aa', 'aaa'], dtype='<U3')
    >>> a = np.array(['a', 'b', 'c', 'd', 'e', 'f']).reshape((2, 3))
    >>> np.strings.multiply(a, 3)
    array([['aaa', 'bbb', 'ccc'],
           ['ddd', 'eee', 'fff']], dtype='<U3')
    >>> np.strings.multiply(a, i)
    array([['a', 'bb', 'ccc'],
           ['d', 'ee', 'fff']], dtype='<U3')

    """
    a = np.asanyarray(a)

    i = np.asanyarray(i)
    if not np.issubdtype(i.dtype, np.integer):
        raise TypeError(f"unsupported type {i.dtype} for operand 'i'")
    i = np.maximum(i, 0)

    # delegate to stringdtype loops that also do overflow checking
    if a.dtype.char == "T":
        return a * i

    a_len = str_len(a)

    # Ensure we can do a_len * i without overflow.
    if np.any(a_len > sys.maxsize / np.maximum(i, 1)):
        raise OverflowError("Overflow encountered in string multiply")

    buffersizes = a_len * i
    out_dtype = f"{a.dtype.char}{buffersizes.max()}"
    out = np.empty_like(a, shape=buffersizes.shape, dtype=out_dtype)
    return _multiply_ufunc(a, i, out=out)


def multiply(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MulOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def multiply(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MulOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def multiply(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Multiply two arrays element-wise.

  JAX implementation of :obj:`numpy.multiply`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``*`` operator for
  JAX arrays.

  Args:
    x, y: arrays to multiply. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise multiplication.

  Examples:
    Calling ``multiply`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.multiply(x, 10)
    Array([ 0, 10, 20, 30], dtype=int32)

    Calling ``multiply`` via the ``*`` operator:

    >>> x * 10
    Array([ 0, 10, 20, 30], dtype=int32)
  """
  x, y = promote_args("multiply", x, y)
  return lax.mul(x, y) if x.dtype != bool else lax.bitwise_and(x, y)

