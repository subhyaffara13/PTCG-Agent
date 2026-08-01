
def take(n, seq):
    """ The first n elements of a sequence

    >>> list(take(2, [10, 20, 30, 40, 50]))
    [10, 20]

    See Also:
        drop
        tail
    """
    return itertools.islice(seq, n)


def take(self, index):
    flattened = self.reshape(-1)
    return flattened[index]


def take(
    a: ArrayLike,
    indices: ArrayLike,
    axis=None,
    out: OutArray | None = None,
    mode: NotImplementedType = "raise",
):
    (a,), axis = _util.axis_none_flatten(a, axis=axis)
    axis = _util.normalize_axis_index(axis, a.ndim)
    idx = (slice(None),) * axis + (indices, ...)
    result = a[idx]
    return result


def take(g: jit_utils.GraphContext, self, index):
    self_flattened = symbolic_helper._reshape_helper(
        g, self, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))
    )
    out = index_select(g, self_flattened, 0, index)
    out = reshape_as(g, out, index)
    return out


def take(iter, n):
    """Return ``n`` items from ``iter`` iterator. """
    return [ value for _, value in zip(range(n), iter) ]


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


def take(n, iterable):
    """Return first *n* items of the *iterable* as a list.

        >>> take(3, range(10))
        [0, 1, 2]

    If there are fewer than *n* items in the iterable, all of them are
    returned.

        >>> take(10, range(3))
        [0, 1, 2]

    """
    return list(islice(iterable, n))


def take(x: Array, indices: Array, /, *, axis: int | None = None, **kwargs: object) -> Array:
    if axis is None:
        if x.ndim != 1:
            raise ValueError("axis must be specified when ndim > 1")
        axis = 0
    # torch does not support negative indices,
    # see https://github.com/pytorch/pytorch/issues/146211
    return torch.index_select(
        x,
        axis,
        torch.where(indices < 0, indices + x.shape[axis], indices),
        **kwargs
    )


def take(
    arr,
    indices: TakeIndexer,
    axis: AxisInt = 0,
    allow_fill: bool = False,
    fill_value=None,
):
    """
    Take elements from an array.

    Parameters
    ----------
    arr : numpy.ndarray, ExtensionArray, Index, or Series
        Input array.
    indices : sequence of int or one-dimensional np.ndarray of int
        Indices to be taken.
    axis : int, default 0
        The axis over which to select values.
    allow_fill : bool, default False
        How to handle negative values in `indices`.

        * False: negative values in `indices` indicate positional indices
          from the right (the default). This is similar to :func:`numpy.take`.

        * True: negative values in `indices` indicate
          missing values. These values are set to `fill_value`. Any other
          negative values raise a ``ValueError``.

    fill_value : any, optional
        Fill value to use for NA-indices when `allow_fill` is True.
        This may be ``None``, in which case the default NA value for
        the type (``self.dtype.na_value``) is used.

        For multi-dimensional `arr`, each *element* is filled with
        `fill_value`.

    Returns
    -------
    ndarray or ExtensionArray
        Same type as the input.

    Raises
    ------
    IndexError
        When `indices` is out of bounds for the array.
    ValueError
        When the indexer contains negative values other than ``-1``
        and `allow_fill` is True.

    Notes
    -----
    When `allow_fill` is False, `indices` may be whatever dimensionality
    is accepted by NumPy for `arr`.

    When `allow_fill` is True, `indices` should be 1-D.

    See Also
    --------
    numpy.take : Take elements from an array along an axis.

    Examples
    --------
    >>> import pandas as pd

    With the default ``allow_fill=False``, negative numbers indicate
    positional indices from the right.

    >>> pd.api.extensions.take(np.array([10, 20, 30]), [0, 0, -1])
    array([10, 10, 30])

    Setting ``allow_fill=True`` will place `fill_value` in those positions.

    >>> pd.api.extensions.take(np.array([10, 20, 30]), [0, 0, -1], allow_fill=True)
    array([10., 10., nan])

    >>> pd.api.extensions.take(
    ...     np.array([10, 20, 30]), [0, 0, -1], allow_fill=True, fill_value=-10
    ... )
    array([ 10,  10, -10])
    """
    if not isinstance(
        arr,
        (np.ndarray, ABCExtensionArray, ABCIndex, ABCSeries, ABCNumpyExtensionArray),
    ):
        # GH#52981
        raise TypeError(
            "pd.api.extensions.take requires a numpy.ndarray, ExtensionArray, "
            f"Index, Series, or NumpyExtensionArray got {type(arr).__name__}."
        )

    indices = ensure_platform_int(indices)

    if allow_fill:
        # Pandas style, -1 means NA
        validate_indices(indices, arr.shape[axis])
        # error: Argument 1 to "take_nd" has incompatible type
        # "ndarray[Any, Any] | ExtensionArray | Index | Series"; expected
        # "ndarray[Any, Any]"
        result = take_nd(
            arr,  # type: ignore[arg-type]
            indices,
            axis=axis,
            allow_fill=True,
            fill_value=fill_value,
        )
    else:
        # NumPy style
        # error: Unexpected keyword argument "axis" for "take" of "ExtensionArray"
        result = arr.take(indices, axis=axis)  # type: ignore[call-arg,assignment]
    return result


def take(a, indices, axis=None, out=None, mode='raise'):
    """

    """
    a = masked_array(a)
    return a.take(indices, axis=axis, out=out, mode=mode)


def take(a, indices, axis=None, out=None, mode='raise'):
    """
    Take elements from an array along an axis.

    When axis is not None, this function does the same thing as "fancy"
    indexing (indexing arrays using arrays); however, it can be easier to use
    if you need elements along a given axis. A call such as
    ``np.take(arr, indices, axis=3)`` is equivalent to
    ``arr[:,:,:,indices,...]``.

    Explained without fancy indexing, this is equivalent to the following use
    of `ndindex`, which sets each of ``ii``, ``jj``, and ``kk`` to a tuple of
    indices::

        Ni, Nk = a.shape[:axis], a.shape[axis+1:]
        Nj = indices.shape
        for ii in ndindex(Ni):
            for jj in ndindex(Nj):
                for kk in ndindex(Nk):
                    out[ii + jj + kk] = a[ii + (indices[jj],) + kk]

    Parameters
    ----------
    a : array_like (Ni..., M, Nk...)
        The source array.
    indices : array_like (Nj...)
        The indices of the values to extract.
        Also allow scalars for indices.
    axis : int, optional
        The axis over which to select values. By default, the flattened
        input array is used.
    out : ndarray, optional (Ni..., Nj..., Nk...)
        If provided, the result will be placed in this array. It should
        be of the appropriate shape and dtype. Note that `out` is always
        buffered if `mode='raise'`; use other modes for better performance.
    mode : {'raise', 'wrap', 'clip'}, optional
        Specifies how out-of-bounds indices will behave.

        * 'raise' -- raise an error (default)
        * 'wrap' -- wrap around
        * 'clip' -- clip to the range

        'clip' mode means that all indices that are too large are replaced
        by the index that addresses the last element along that axis. Note
        that this disables indexing with negative numbers.

    Returns
    -------
    out : ndarray (Ni..., Nj..., Nk...)
        The returned array has the same type as `a`.

    See Also
    --------
    compress : Take elements using a boolean mask
    ndarray.take : equivalent method
    take_along_axis : Take elements by matching the array and the index arrays

    Notes
    -----
    By eliminating the inner loop in the description above, and using `s_` to
    build simple slice objects, `take` can be expressed  in terms of applying
    fancy indexing to each 1-d slice::

        Ni, Nk = a.shape[:axis], a.shape[axis+1:]
        for ii in ndindex(Ni):
            for kk in ndindex(Nk):
                out[ii + s_[...,] + kk] = a[ii + s_[:,] + kk][indices]

    For this reason, it is equivalent to (but faster than) the following use
    of `apply_along_axis`::

        out = np.apply_along_axis(lambda a_1d: a_1d[indices], axis, a)

    Examples
    --------
    >>> import numpy as np
    >>> a = [4, 3, 5, 7, 6, 8]
    >>> indices = [0, 1, 4]
    >>> np.take(a, indices)
    array([4, 3, 6])

    In this example if `a` is an ndarray, "fancy" indexing can be used.

    >>> a = np.array(a)
    >>> a[indices]
    array([4, 3, 6])

    If `indices` is not one dimensional, the output also has these dimensions.

    >>> np.take(a, [[0, 1], [2, 3]])
    array([[4, 3],
           [5, 7]])
    """
    return _wrapfunc(a, 'take', indices, axis=axis, out=out, mode=mode)


def take(
    a: ArrayLike,
    indices: ArrayLike,
    axis: int | None = None,
    out: None = None,
    mode: str | None = None,
    unique_indices: bool = False,
    indices_are_sorted: bool = False,
    fill_value: StaticScalar | None = None,
) -> Array:
  """Take elements from an array.

  JAX implementation of :func:`numpy.take`, implemented in terms of
  :func:`jax.lax.gather`. JAX's behavior differs from NumPy in the case
  of out-of-bound indices; see the ``mode`` parameter below.

  Args:
    a: array from which to take values.
    indices: N-dimensional array of integer indices of values to take from the array.
    axis: the axis along which to take values. If not specified, the array will
      be flattened before indexing is applied.
    mode: Out-of-bounds indexing mode, either ``"fill"`` or ``"clip"``. The default
      ``mode="fill"`` returns invalid values (e.g. NaN) for out-of bounds indices;
      the ``fill_value`` argument gives control over this value. For more discussion
      of ``mode`` options, see :attr:`jax.numpy.ndarray.at`.
    fill_value: The fill value to return for out-of-bounds slices when mode is 'fill'.
      Ignored otherwise. Defaults to NaN for inexact types, the largest negative value for
      signed types, the largest positive value for unsigned types, and True for booleans.
    unique_indices: If True, the implementation will assume that the indices are unique
      after normalization of negative indices, which lets the compiler emit more efficient
      code during the backward pass. If set to True and normalized indices are not unique,
      the result is implementation-defined and may be non-deterministic.
    indices_are_sorted : If True, the implementation will assume that the indices are
      sorted in ascending order after normalization of negative indices, which can lead
      to more efficient execution on some backends. If set to True and normalized indices
      are not sorted, the output is implementation-defined.

  Returns:
    Array of values extracted from ``a``.

  See also:
    - :attr:`jax.numpy.ndarray.at`: take values via indexing syntax.
    - :func:`jax.numpy.take_along_axis`: take values along an axis

  Examples:
    >>> x = jnp.array([[1., 2., 3.],
    ...                [4., 5., 6.]])
    >>> indices = jnp.array([2, 0])

    Passing no axis results in indexing into the flattened array:

    >>> jnp.take(x, indices)
    Array([3., 1.], dtype=float32)
    >>> x.ravel()[indices]  # equivalent indexing syntax
    Array([3., 1.], dtype=float32)

    Passing an axis results ind applying the index to every subarray along the axis:

    >>> jnp.take(x, indices, axis=1)
    Array([[3., 1.],
           [6., 4.]], dtype=float32)
    >>> x[:, indices]  # equivalent indexing syntax
    Array([[3., 1.],
           [6., 4.]], dtype=float32)

    Out-of-bound indices fill with invalid values. For float inputs, this is `NaN`:

    >>> jnp.take(x, indices, axis=0)
    Array([[nan, nan, nan],
           [ 1.,  2.,  3.]], dtype=float32)
    >>> x.at[indices].get(mode='fill', fill_value=jnp.nan)  # equivalent indexing syntax
    Array([[nan, nan, nan],
           [ 1.,  2.,  3.]], dtype=float32)

    This default out-of-bound behavior can be adjusted using the ``mode`` parameter, for
    example, we can instead clip to the last valid value:

    >>> jnp.take(x, indices, axis=0, mode='clip')
    Array([[4., 5., 6.],
           [1., 2., 3.]], dtype=float32)
    >>> x.at[indices].get(mode='clip')  # equivalent indexing syntax
    Array([[4., 5., 6.],
           [1., 2., 3.]], dtype=float32)
  """
  return _take(a, indices, None if axis is None else operator.index(axis), out,
               mode, unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
               fill_value=fill_value)


def take(env_state):
    """This function is called if the player has decided to take a card."""
    state, key = env_state
    dealer_hand = state.dealer_hand
    player_hand = state.player_hand
    dealer_cards = state.dealer_cards
    player_cards = state.player_cards
    key, new_player_hand, _ = draw_card(key, player_hand, player_cards)
    new_player_cards = player_cards + 1

    # done is set to zero here because it is determined later whether the player is bust

    return (
        EnvState(
            dealer_hand=dealer_hand,
            player_hand=new_player_hand,
            dealer_cards=dealer_cards,
            player_cards=new_player_cards,
            done=0,
        ),
        key,
    )

