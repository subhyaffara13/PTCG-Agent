
def trim_zeros(filt, trim='fb', axis=None):
    """Remove values along a dimension which are zero along all other.

    Parameters
    ----------
    filt : array_like
        Input array.
    trim : {"fb", "f", "b"}, optional
        A string with 'f' representing trim from front and 'b' to trim from
        back. By default, zeros are trimmed on both sides.
        Front and back refer to the edges of a dimension, with "front" referring
        to the side with the lowest index 0, and "back" referring to the highest
        index (or index -1).
    axis : int or sequence, optional
        If None, `filt` is cropped such that the smallest bounding box is
        returned that still contains all values which are not zero.
        If an axis is specified, `filt` will be sliced in that dimension only
        on the sides specified by `trim`. The remaining area will be the
        smallest that still contains all values which are not zero.

        .. versionadded:: 2.2.0

    Returns
    -------
    trimmed : ndarray or sequence
        The result of trimming the input. The number of dimensions and the
        input data type are preserved.

    Notes
    -----
    For all-zero arrays, the first axis is trimmed first.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array((0, 0, 0, 1, 2, 3, 0, 2, 1, 0))
    >>> np.trim_zeros(a)
    array([1, 2, 3, 0, 2, 1])

    >>> np.trim_zeros(a, trim='b')
    array([0, 0, 0, ..., 0, 2, 1])

    Multiple dimensions are supported.

    >>> b = np.array([[0, 0, 2, 3, 0, 0],
    ...               [0, 1, 0, 3, 0, 0],
    ...               [0, 0, 0, 0, 0, 0]])
    >>> np.trim_zeros(b)
    array([[0, 2, 3],
           [1, 0, 3]])

    >>> np.trim_zeros(b, axis=-1)
    array([[0, 2, 3],
           [1, 0, 3],
           [0, 0, 0]])

    The input data type is preserved, list/tuple in means list/tuple out.

    >>> np.trim_zeros([0, 1, 2, 0])
    [1, 2]

    """
    filt_ = np.asarray(filt)

    trim = trim.lower()
    if trim not in {"fb", "bf", "f", "b"}:
        raise ValueError(f"unexpected character(s) in `trim`: {trim!r}")
    if axis is None:
        axis_tuple = tuple(range(filt_.ndim))
    else:
        axis_tuple = _nx.normalize_axis_tuple(axis, filt_.ndim, argname="axis")

    if not axis_tuple:
        # No trimming requested -> return input unmodified.
        return filt

    start, stop = _arg_trim_zeros(filt_)
    stop += 1  # Adjust for slicing

    if start.size == 0:
        # filt is all-zero -> assign same values to start and stop so that
        # resulting slice will be empty
        start = stop = np.zeros(filt_.ndim, dtype=np.intp)
    else:
        if 'f' not in trim:
            start = (None,) * filt_.ndim
        if 'b' not in trim:
            stop = (None,) * filt_.ndim

    sl = tuple(slice(start[ax], stop[ax]) if ax in axis_tuple else slice(None)
               for ax in range(filt_.ndim))
    if len(sl) == 1:
        # filt is 1D -> avoid multi-dimensional slicing to preserve
        # non-array input types
        return filt[sl[0]]
    return filt[sl]


def trim_zeros(filt: ArrayLike, trim: str ='fb',
               axis: int | Sequence[int] | None = None) -> Array:
  """Trim leading and/or trailing zeros of the input array.

  JAX implementation of :func:`numpy.trim_zeros`.

  Args:
    filt: N-dimensional input array.
    trim: string, optional, default = ``fb``. Specifies from which end the input
      is trimmed.

      - ``f`` - trims only the leading zeros.
      - ``b`` - trims only the trailing zeros.
      - ``fb`` - trims both leading and trailing zeros.

    axis: optional axis or axes along which to trim. If not specified, trim along
      all axes of the array.

  Returns:
    An array containing the trimmed input with same dtype as ``filt``.

  Examples:
    One-dimensional input:

    >>> x = jnp.array([0, 0, 2, 0, 1, 4, 3, 0, 0, 0])
    >>> jnp.trim_zeros(x)
    Array([2, 0, 1, 4, 3], dtype=int32)
    >>> jnp.trim_zeros(x, trim='f')
    Array([2, 0, 1, 4, 3, 0, 0, 0], dtype=int32)
    >>> jnp.trim_zeros(x, trim='b')
    Array([0, 0, 2, 0, 1, 4, 3], dtype=int32)

    Two-dimensional input:

    >>> x = jnp.zeros((4, 5)).at[1:3, 1:4].set(1)
    >>> x
    Array([[0., 0., 0., 0., 0.],
           [0., 1., 1., 1., 0.],
           [0., 1., 1., 1., 0.],
           [0., 0., 0., 0., 0.]], dtype=float32)
    >>> jnp.trim_zeros(x)
    Array([[1., 1., 1.],
           [1., 1., 1.]], dtype=float32)
    >>> jnp.trim_zeros(x, trim='f')
    Array([[1., 1., 1., 0.],
           [1., 1., 1., 0.],
           [0., 0., 0., 0.]], dtype=float32)
    >>> jnp.trim_zeros(x, axis=0)
    Array([[0., 1., 1., 1., 0.],
           [0., 1., 1., 1., 0.]], dtype=float32)
    >>> jnp.trim_zeros(x, axis=1)
    Array([[0., 0., 0.],
           [1., 1., 1.],
           [1., 1., 1.],
           [0., 0., 0.]], dtype=float32)
  """
  filt = util.ensure_arraylike("trim_zeros", filt)
  core.concrete_or_error(None, filt,
                         "Error arose in the `filt` argument of trim_zeros()")
  axis_set = set(_canonicalize_axis_tuple(axis, filt.ndim))
  if not axis_set or ('f' not in trim.lower() and 'b' not in trim.lower()):
    return filt
  def _get_slice(x: Array, ax: int) -> slice:
    if ax not in axis_set:
      return slice(None)
    mask = x.any(axis=[i for i in range(x.ndim) if i != ax])
    if not mask.any():
      return slice(0, 0)
    start = int(mask.argmax()) if 'f' in trim.lower() else None
    stop = x.shape[ax] - int(mask[::-1].argmax()) if 'b' in trim.lower() else None
    return slice(start, stop)
  return filt[*(_get_slice(filt, ax) for ax in range(filt.ndim))]

