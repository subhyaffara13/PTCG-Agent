
def choose(
    a: ArrayLike,
    choices: Sequence[ArrayLike],
    out: OutArray | None = None,
    mode: NotImplementedType = "raise",
):
    # First, broadcast elements of `choices`
    choices = torch.stack(torch.broadcast_tensors(*choices))

    # Use an analog of `gather(choices, 0, a)` which broadcasts `choices` vs `a`:
    # (taken from https://github.com/pytorch/pytorch/issues/9407#issuecomment-1427907939)
    idx_list = [
        torch.arange(dim).view((1,) * i + (dim,) + (1,) * (choices.ndim - i - 1))
        for i, dim in enumerate(choices.shape)
    ]

    idx_list[0] = a
    return choices[tuple(idx_list)].squeeze(0)


def choose(indices, choices, out=None, mode='raise'):
    """
    Use an index array to construct a new array from a list of choices.

    Given an array of integers and a list of n choice arrays, this method
    will create a new array that merges each of the choice arrays.  Where a
    value in `index` is i, the new array will have the value that choices[i]
    contains in the same place.

    Parameters
    ----------
    indices : ndarray of ints
        This array must contain integers in ``[0, n-1]``, where n is the
        number of choices.
    choices : sequence of arrays
        Choice arrays. The index array and all of the choices should be
        broadcastable to the same shape.
    out : array, optional
        If provided, the result will be inserted into this array. It should
        be of the appropriate shape and `dtype`.
    mode : {'raise', 'wrap', 'clip'}, optional
        Specifies how out-of-bounds indices will behave.

        * 'raise' : raise an error
        * 'wrap' : wrap around
        * 'clip' : clip to the range

    Returns
    -------
    merged_array : array

    See Also
    --------
    choose : equivalent function

    Examples
    --------
    >>> import numpy as np
    >>> choice = np.array([[1,1,1], [2,2,2], [3,3,3]])
    >>> a = np.array([2, 1, 0])
    >>> np.ma.choose(a, choice)
    masked_array(data=[3, 2, 1],
                 mask=False,
           fill_value=999999)

    """
    def fmask(x):
        "Returns the filled array, or True if masked."
        if x is masked:
            return True
        return filled(x)

    def nmask(x):
        "Returns the mask, True if ``masked``, False if ``nomask``."
        if x is masked:
            return True
        return getmask(x)
    # Get the indices.
    c = filled(indices, 0)
    # Get the masks.
    masks = [nmask(x) for x in choices]
    data = [fmask(x) for x in choices]
    # Construct the mask
    outputmask = np.choose(c, masks, mode=mode)
    outputmask = make_mask(mask_or(outputmask, getmask(indices)),
                           copy=False, shrink=True)
    # Get the choices.
    d = np.choose(c, data, mode=mode, out=out).view(MaskedArray)
    if out is not None:
        if isinstance(out, MaskedArray):
            out.__setmask__(outputmask)
        return out
    d.__setmask__(outputmask)
    return d


def choose(a, choices, out=None, mode='raise'):
    """
    Construct an array from an index array and a list of arrays to choose from.

    First of all, if confused or uncertain, definitely look at the Examples -
    in its full generality, this function is less simple than it might
    seem from the following code description::

        np.choose(a,c) == np.array([c[a[I]][I] for I in np.ndindex(a.shape)])

    But this omits some subtleties.  Here is a fully general summary:

    Given an "index" array (`a`) of integers and a sequence of ``n`` arrays
    (`choices`), `a` and each choice array are first broadcast, as necessary,
    to arrays of a common shape; calling these *Ba* and *Bchoices[i], i =
    0,...,n-1* we have that, necessarily, ``Ba.shape == Bchoices[i].shape``
    for each ``i``.  Then, a new array with shape ``Ba.shape`` is created as
    follows:

    * if ``mode='raise'`` (the default), then, first of all, each element of
      ``a`` (and thus ``Ba``) must be in the range ``[0, n-1]``; now, suppose
      that ``i`` (in that range) is the value at the ``(j0, j1, ..., jm)``
      position in ``Ba`` - then the value at the same position in the new array
      is the value in ``Bchoices[i]`` at that same position;

    * if ``mode='wrap'``, values in `a` (and thus `Ba`) may be any (signed)
      integer; modular arithmetic is used to map integers outside the range
      `[0, n-1]` back into that range; and then the new array is constructed
      as above;

    * if ``mode='clip'``, values in `a` (and thus ``Ba``) may be any (signed)
      integer; negative integers are mapped to 0; values greater than ``n-1``
      are mapped to ``n-1``; and then the new array is constructed as above.

    Parameters
    ----------
    a : int array
        This array must contain integers in ``[0, n-1]``, where ``n`` is the
        number of choices, unless ``mode=wrap`` or ``mode=clip``, in which
        cases any integers are permissible.
    choices : sequence of arrays
        Choice arrays. `a` and all of the choices must be broadcastable to the
        same shape.  If `choices` is itself an array (not recommended), then
        its outermost dimension (i.e., the one corresponding to
        ``choices.shape[0]``) is taken as defining the "sequence".
    out : array, optional
        If provided, the result will be inserted into this array. It should
        be of the appropriate shape and dtype. Note that `out` is always
        buffered if ``mode='raise'``; use other modes for better performance.
    mode : {'raise' (default), 'wrap', 'clip'}, optional
        Specifies how indices outside ``[0, n-1]`` will be treated:

        * 'raise' : an exception is raised
        * 'wrap' : value becomes value mod ``n``
        * 'clip' : values < 0 are mapped to 0, values > n-1 are mapped to n-1

    Returns
    -------
    merged_array : array
        The merged result.

    Raises
    ------
    ValueError: shape mismatch
        If `a` and each choice array are not all broadcastable to the same
        shape.

    See Also
    --------
    ndarray.choose : equivalent method
    numpy.take_along_axis : Preferable if `choices` is an array

    Notes
    -----
    To reduce the chance of misinterpretation, even though the following
    "abuse" is nominally supported, `choices` should neither be, nor be
    thought of as, a single array, i.e., the outermost sequence-like container
    should be either a list or a tuple.

    Examples
    --------

    >>> import numpy as np
    >>> choices = [[0, 1, 2, 3], [10, 11, 12, 13],
    ...   [20, 21, 22, 23], [30, 31, 32, 33]]
    >>> np.choose([2, 3, 1, 0], choices
    ... # the first element of the result will be the first element of the
    ... # third (2+1) "array" in choices, namely, 20; the second element
    ... # will be the second element of the fourth (3+1) choice array, i.e.,
    ... # 31, etc.
    ... )
    array([20, 31, 12,  3])
    >>> np.choose([2, 4, 1, 0], choices, mode='clip') # 4 goes to 3 (4-1)
    array([20, 31, 12,  3])
    >>> # because there are 4 choice arrays
    >>> np.choose([2, 4, 1, 0], choices, mode='wrap') # 4 goes to (4 mod 4)
    array([20,  1, 12,  3])
    >>> # i.e., 0

    A couple examples illustrating how choose broadcasts:

    >>> a = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    >>> choices = [-10, 10]
    >>> np.choose(a, choices)
    array([[ 10, -10,  10],
           [-10,  10, -10],
           [ 10, -10,  10]])

    >>> # With thanks to Anne Archibald
    >>> a = np.array([0, 1]).reshape((2,1,1))
    >>> c1 = np.array([1, 2, 3]).reshape((1,3,1))
    >>> c2 = np.array([-1, -2, -3, -4, -5]).reshape((1,1,5))
    >>> np.choose(a, (c1, c2)) # result is 2x3x5, res[0,:,:]=c1, res[1,:,:]=c2
    array([[[ 1,  1,  1,  1,  1],
            [ 2,  2,  2,  2,  2],
            [ 3,  3,  3,  3,  3]],
           [[-1, -2, -3, -4, -5],
            [-1, -2, -3, -4, -5],
            [-1, -2, -3, -4, -5]]])

    """
    return _wrapfunc(a, 'choose', choices, out=out, mode=mode)


def choose(a: ArrayLike, choices: Array | np.ndarray | Sequence[ArrayLike],
           out: None = None, mode: str = 'raise') -> Array:
  """Construct an array by stacking slices of choice arrays.

  JAX implementation of :func:`numpy.choose`.

  The semantics of this function can be confusing, but in the simplest case where
  ``a`` is a one-dimensional array, ``choices`` is a two-dimensional array, and
  all entries of ``a`` are in-bounds (i.e. ``0 <= a_i < len(choices)``), then the
  function is equivalent to the following::

     def choose(a, choices):
       return jnp.array([choices[a_i, i] for i, a_i in enumerate(a)])

  In the more general case, ``a`` may have any number of dimensions and ``choices``
  may be an arbitrary sequence of broadcast-compatible arrays. In this case, again
  for in-bound indices, the logic is equivalent to::

     def choose(a, choices):
       a, *choices = jnp.broadcast_arrays(a, *choices)
       choices = jnp.array(choices)
       return jnp.array([choices[a[idx], *idx] for idx in np.ndindex(a.shape)])

  The only additional complexity comes from the ``mode`` argument, which controls
  the behavior for out-of-bound indices in ``a`` as described below.

  Args:
    a: an N-dimensional array of integer indices.
    choices: an array or sequence of arrays. All arrays in the sequence must be
      mutually broadcast compatible with ``a``.
    out: unused by JAX
    mode: specify the out-of-bounds indexing mode; one of ``'raise'`` (default),
      ``'wrap'``, or ``'clip'``. Note that the default mode of ``'raise'`` is
      not compatible with JAX transformations.

  Returns:
    an array containing stacked slices from ``choices`` at the indices
    specified by ``a``. The shape of the result is
    ``broadcast_shapes(a.shape, *(c.shape for c in choices))``.

  See also:
    - :func:`jax.lax.switch`: choose between N functions based on an index.

  Examples:
    Here is the simplest case of a 1D index array with a 2D choice array,
    in which case this chooses the indexed value from each column:

    >>> choices = jnp.array([[ 1,  2,  3,  4],
    ...                      [ 5,  6,  7,  8],
    ...                      [ 9, 10, 11, 12]])
    >>> a = jnp.array([2, 0, 1, 0])
    >>> jnp.choose(a, choices)
    Array([9, 2, 7, 4], dtype=int32)

    The ``mode`` argument specifies what to do with out-of-bound indices;
    options are to either ``wrap`` or ``clip``:

    >>> a2 = jnp.array([2, 0, 1, 4])  # last index out-of-bound
    >>> jnp.choose(a2, choices, mode='clip')
    Array([ 9,  2,  7, 12], dtype=int32)
    >>> jnp.choose(a2, choices, mode='wrap')
    Array([9, 2, 7, 8], dtype=int32)

    In the more general case, ``choices`` may be a sequence of array-like
    objects with any broadcast-compatible shapes.

    >>> choice_1 = jnp.array([1, 2, 3, 4])
    >>> choice_2 = 99
    >>> choice_3 = jnp.array([[10],
    ...                       [20],
    ...                       [30]])
    >>> a = jnp.array([[0, 1, 2, 0],
    ...                [1, 2, 0, 1],
    ...                [2, 0, 1, 2]])
    >>> jnp.choose(a, [choice_1, choice_2, choice_3], mode='wrap')
    Array([[ 1, 99, 10,  4],
           [99, 20,  3, 99],
           [30,  2, 99, 30]], dtype=int32)
  """
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.choose is not supported.")
  a, *choices = util.ensure_arraylike_tuple('choose', (a, *choices))
  if not issubdtype(a.dtype, np.integer):
    raise ValueError("`a` array must be integer typed")
  N = len(choices)

  if mode == 'raise':
    arr: Array = core.concrete_or_error(asarray, a,
      "The error occurred because jnp.choose was jit-compiled"
      " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if reductions.any((arr < 0) | (arr >= N)):
      raise ValueError("invalid entry in choice array")
  elif mode == 'wrap':
    arr = asarray(a) % N
  elif mode == 'clip':
    arr = clip(a, 0, N - 1)
  else:
    raise ValueError(f"mode={mode!r} not understood. Must be 'raise', 'wrap', or 'clip'")

  arr, *choices = broadcast_arrays(arr, *choices)
  return array(choices)[(arr,) + indices(arr.shape, sparse=True)]

