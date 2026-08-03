import functools
import math


def searchsorted(
    sorted_sequence: TensorBox,
    self: TensorBox,
    *,
    out_int32: bool = False,
    right: bool = False,
    side: str | None = None,
    sorter: TensorBox | None = None,
) -> TensorBox:
    validate_bucketize = lambda tb: V.graph.has_feature(  # noqa: E731
        tb, BackendFeature.BUCKETIZE
    )
    if (
        not validate_bucketize(sorted_sequence)
        or not validate_bucketize(self)
        or (sorter is not None and not validate_bucketize(sorter))
    ):
        return fallback_handler(aten.searchsorted.Tensor, add_to_fallback_set=False)(
            sorted_sequence,
            self,
            out_int32=out_int32,
            right=right,
            side=side,
            sorter=sorter,
        )

    # If side is present, override the value of right if needed.  This assumes that
    # validation of the two options being non-contradictory is already done by the
    # searchsorted meta-function.
    if side is not None and side == "right":
        right = True

    index_dtype = torch.int32 if out_int32 else torch.int64
    values_loader = self.make_loader()

    # The entire sorted_sequence tensor needs to be used by ops.bucketize, so we need to
    # realize it into global memory; or in other words, we can't guarantee that
    # sorted_sequence.get_name() (used below) will exist unless we call
    # sorted_sequence.realize().
    sorted_sequence.realize()

    if sorter is not None:
        sorter.realize()

    if len(sorted_sequence.get_size()) == 1:

        def inner_fn(idx):
            val = values_loader(idx)
            return ops.bucketize(
                val,
                _boundaries_helper(sorted_sequence),
                0,
                index_dtype,
                right,
                sorter=None if sorter is None else _sorter_helper(sorter),
                sorter_indices=None if sorter is None else 0,
            )

    else:

        def inner_fn(idx):
            val = values_loader(idx)

            # Get index to the beginning of the sorted sequence within a flattened
            # version of the array.
            def get_flattened_index(tb: TensorBox):
                strides = tb.get_stride()
                return ops.index_expr(
                    functools.reduce(
                        operator.add, (s * i for s, i in zip(strides[:-1], idx[:-1]))
                    ),
                    index_dtype,
                )

            return ops.bucketize(
                val,
                _boundaries_helper(sorted_sequence),
                get_flattened_index(sorted_sequence),
                index_dtype,
                right,
                sorter=None if sorter is None else _sorter_helper(sorter),
                sorter_indices=None if sorter is None else get_flattened_index(sorter),
            )

    device = self.get_device()
    result = Pointwise.create(
        device=device,
        dtype=index_dtype,
        inner_fn=inner_fn,
        ranges=self.shape,
    )
    # see [NOTE: inductor bucketize realize]
    result.realize()

    return result


def searchsorted(
    a: ArrayLike, v: ArrayLike, side="left", sorter: ArrayLike | None = None
):
    if a.dtype.is_complex:
        raise NotImplementedError(f"searchsorted with dtype={a.dtype}")

    return torch.searchsorted(a, v, side=side, sorter=sorter)


def searchsorted(
    x1: Array,
    x2: Array,
    /,
    *,
    side: Literal["left", "right"] = "left",
    xp: ModuleType | None = None,
) -> Array:
    """
    Find indices where elements should be inserted to maintain order.

    Find the indices into a sorted array ``x1`` such that if the elements in ``x2``
    were inserted before the indices, the resulting array would remain sorted.

    The behavior of this function is similar to that of `array_api.searchsorted`,
    but it relaxes the requirement that `x1` must be one-dimensional.
    This function is vectorized, treating slices along the last axis
    as elements and preceding axes as batch (or "loop") dimensions.

    Parameters
    ----------
    x1 : Array
        Input array. Should have a real-valued data type. Must be sorted in ascending
        order along the last axis.
    x2 : Array
        Array containing search values. Should have a real-valued data type. Must have
        the same shape as ``x1`` except along the last axis.
    side : {'left', 'right'}, optional
        Argument controlling which index is returned if an element of ``x2`` is equal to
        one or more elements of ``x1``: ``'left'`` returns the index of the first of
        these elements; ``'right'`` returns the next index after the last of these
        elements. Default: ``'left'``.
    xp : array_namespace, optional
        The standard-compatible namespace for the array arguments. Default: infer.

    Returns
    -------
    Array: integer array
        An array of indices with the same shape as ``x2``.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> x = xp.asarray([11, 12, 13, 13, 14, 15])
    >>> xpx.searchsorted(x, xp.asarray([10, 11.5, 14.5, 16]), xp=xp)
    Array([0, 1, 5, 6], dtype=array_api_strict.int64)
    >>> xpx.searchsorted(x, xp.asarray(13), xp=xp)
    Array(2, dtype=array_api_strict.int64)
    >>> xpx.searchsorted(x, xp.asarray(13), side='right', xp=xp)
    Array(4, dtype=array_api_strict.int64)

    `searchsorted` is vectorized along the last axis.

    >>> x1 = xp.asarray([[1., 2., 3., 4.], [5., 6., 7., 8.]])
    >>> x2 = xp.asarray([[1.1, 3.3], [6.6, 8.8]])
    >>> xpx.searchsorted(x1, x2, xp=xp)
    Array([[1, 3],
           [2, 4]], dtype=array_api_strict.int64)
    """
    if xp is None:
        xp = array_namespace(x1, x2)

    if side not in {"left", "right"}:
        message = "`side` must be either 'left' or 'right'."
        raise ValueError(message)

    xp_default_int = _funcs.default_dtype(xp, kind="integral")
    x2_0d = x2.ndim == 0
    x1_1d = x1.ndim <= 1

    if x1_1d or is_torch_namespace(xp):
        x2 = xp.reshape(x2, ()) if (x2_0d and x1_1d) else x2
        out = xp.searchsorted(x1, x2, side=side)
        return xp.astype(out, xp_default_int, copy=False)

    return _funcs.searchsorted(x1, x2, side=side, xp=xp)


def searchsorted(
    x1: Array,
    x2: Array,
    /,
    *,
    side: Literal["left", "right"] = "left",
    xp: ModuleType,
) -> Array:
    # numpydoc ignore=PR01,RT01
    """See docstring in `array_api_extra._delegation.py`."""
    a = xp.full(x2.shape, 0, device=_compat.device(x1))

    if x1.shape[-1] == 0:
        return a

    n = xp.count_nonzero(~xp.isnan(x1), axis=-1, keepdims=True)
    b = xp.broadcast_to(n, x2.shape)

    compare = xp.less_equal if side == "left" else xp.less

    # while xp.any(b - a > 1):
    # refactored to for loop with ~log2(n) iterations for JAX JIT
    for _ in range(int(math.log2(x1.shape[-1])) + 1):  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        c = (a + b) // 2
        x0 = xp.take_along_axis(x1, c, axis=-1)
        j = compare(x2, x0)
        b = xp.where(j, c, b)
        a = xp.where(j, a, c)

    out = xp.where(compare(x2, xp.min(x1, axis=-1, keepdims=True)), 0, b)
    out = xp.where(xp.isnan(x2), x1.shape[-1], out) if side == "right" else out
    return xp.astype(out, default_dtype(xp, kind="integral"), copy=False)


def searchsorted(
    x1: Array,
    x2: Array | int | float,
    /,
    *,
    side: Literal['left', 'right'] = 'left',
    sorter: Array | None = None
) -> Array:
    if not isinstance(x2, cp.ndarray):
        if not isinstance(x2, int | float | complex):
            raise NotImplementedError(
                'Only python scalars or ndarrays are supported for x2')
        x2 = cp.asarray(x2)
    return cp.searchsorted(x1, x2, side, sorter)


def searchsorted(
    arr: ArrayLike,
    value: NumpyValueArrayLike | ExtensionArray,
    side: Literal["left", "right"] = "left",
    sorter: NumpySorter | None = None,
) -> npt.NDArray[np.intp] | np.intp:
    """
    Find indices where elements should be inserted to maintain order.

    Find the indices into a sorted array `arr` (a) such that, if the
    corresponding elements in `value` were inserted before the indices,
    the order of `arr` would be preserved.

    Assuming that `arr` is sorted:

    ======  ================================
    `side`  returned index `i` satisfies
    ======  ================================
    left    ``arr[i-1] < value <= self[i]``
    right   ``arr[i-1] <= value < self[i]``
    ======  ================================

    Parameters
    ----------
    arr: np.ndarray, ExtensionArray, Series
        Input array. If `sorter` is None, then it must be sorted in
        ascending order, otherwise `sorter` must be an array of indices
        that sort it.
    value : array-like or scalar
        Values to insert into `arr`.
    side : {'left', 'right'}, optional
        If 'left', the index of the first suitable location found is given.
        If 'right', return the last such index.  If there is no suitable
        index, return either 0 or N (where N is the length of `self`).
    sorter : 1-D array-like, optional
        Optional array of integer indices that sort array a into ascending
        order. They are typically the result of argsort.

    Returns
    -------
    array of ints or int
        If value is array-like, array of insertion points.
        If value is scalar, a single integer.

    See Also
    --------
    numpy.searchsorted : Similar method from NumPy.
    """
    if sorter is not None:
        sorter = ensure_platform_int(sorter)

    if (
        isinstance(arr, np.ndarray)
        and arr.dtype.kind in "iu"
        and (is_integer(value) or is_integer_dtype(value))
    ):
        # if `arr` and `value` have different dtypes, `arr` would be
        # recast by numpy, causing a slow search.
        # Before searching below, we therefore try to give `value` the
        # same dtype as `arr`, while guarding against integer overflows.
        iinfo = np.iinfo(arr.dtype.type)
        value_arr = np.array([value]) if is_integer(value) else np.array(value)
        if (value_arr >= iinfo.min).all() and (value_arr <= iinfo.max).all():
            # value within bounds, so no overflow, so can convert value dtype
            # to dtype of arr
            dtype = arr.dtype
        else:
            dtype = value_arr.dtype

        if is_integer(value):
            # We know that value is int
            value = cast(int, dtype.type(value))
        else:
            value = pd_array(cast(ArrayLike, value), dtype=dtype)
    else:
        # E.g. if `arr` is an array with dtype='datetime64[ns]'
        # and `value` is a pd.Timestamp, we may need to convert value
        arr = ensure_wrapped_if_datetimelike(arr)

    # Argument 1 to "searchsorted" of "ndarray" has incompatible type
    # "Union[NumpyValueArrayLike, ExtensionArray]"; expected "NumpyValueArrayLike"
    return arr.searchsorted(value, side=side, sorter=sorter)  # type: ignore[arg-type]


def searchsorted(a, v, side='left', sorter=None):
    """
    Find indices where elements should be inserted to maintain order.

    Find the indices into a sorted array `a` such that, if the
    corresponding elements in `v` were inserted before the indices, the
    order of `a` would be preserved.

    Assuming that `a` is sorted:

    ======  ============================
    `side`  returned index `i` satisfies
    ======  ============================
    left    ``a[i-1] < v <= a[i]``
    right   ``a[i-1] <= v < a[i]``
    ======  ============================

    Parameters
    ----------
    a : 1-D array_like
        Input array. If `sorter` is None, then it must be sorted in
        ascending order, otherwise `sorter` must be an array of indices
        that sort it.
    v : array_like
        Values to insert into `a`.
    side : {'left', 'right'}, optional
        If 'left', the index of the first suitable location found is given.
        If 'right', return the last such index.  If there is no suitable
        index, return either 0 or N (where N is the length of `a`).
    sorter : 1-D array_like, optional
        Optional array of integer indices that sort array a into ascending
        order. They are typically the result of argsort.

    Returns
    -------
    indices : int or array of ints
        Array of insertion points with the same shape as `v`,
        or an integer if `v` is a scalar.

    See Also
    --------
    sort : Return a sorted copy of an array.
    histogram : Produce histogram from 1-D data.

    Notes
    -----
    Binary search is used to find the required insertion points.

    As of NumPy 1.4.0 `searchsorted` works with real/complex arrays containing
    `nan` values. The enhanced sort order is documented in `sort`.

    This function uses the same algorithm as the builtin python
    `bisect.bisect_left` (``side='left'``) and `bisect.bisect_right`
    (``side='right'``) functions, which is also vectorized
    in the `v` argument.

    Examples
    --------
    >>> import numpy as np
    >>> np.searchsorted([11,12,13,14,15], 13)
    2
    >>> np.searchsorted([11,12,13,14,15], 13, side='right')
    3
    >>> np.searchsorted([11,12,13,14,15], [-10, 20, 12, 13])
    array([0, 5, 1, 2])

    When `sorter` is used, the returned indices refer to the sorted
    array of `a` and not `a` itself:

    >>> a = np.array([40, 10, 20, 30])
    >>> sorter = np.argsort(a)
    >>> sorter
    array([1, 2, 3, 0])  # Indices that would sort the array 'a'
    >>> result = np.searchsorted(a, 25, sorter=sorter)
    >>> result
    2
    >>> a[sorter[result]]
    30  # The element at index 2 of the sorted array is 30.
    """
    return _wrapfunc(a, 'searchsorted', v, side=side, sorter=sorter)


def searchsorted(
    sorted_arr: ArrayLike,
    query: ArrayLike,
    /,
    *,
    side: str = "left",
    dimension: int = 0,
    batch_dims: int = 0,
    method: str = "scan",
    dtype: DTypeLike = "int32",
):
  """Find indices of query values within a sorted array.

  This is a batch-aware implementation of :func:`numpy.searchsorted` built on a
  HiJAX primitive. It adds the `batch_dims` and `dimension` argument, which make
  the API closed under batching.

  Args:
    sorted_arr: N-dimensional array, which is assumed to be sorted in increasing
      order along ``dimension``.
    query: N-dimensional array of query values.
    side: 'left' (default) or 'right'. If 'left', find the index of the first
      suitable location. If 'right', find the index of the last.
    dimension: positive integer specifying the dimension of ``sorted_arr`` along
      which to insert query values. Defaults to the first dimension.
    batch_dims: integer specifying the number of leading dimensions of
      ``sorted_arr`` and ``query`` to treat as shared batch dimensions.
      Defaults to zero.
    method: string specifying the search method: one of 'scan' (default),
      'compare_all', or 'sort'. 'scan' uses a scan-based binary search implementation,
      'compare_all' directly compares all elements in `sorted_arr` to `query`, and
      'sort' uses a cosorting-based implementation.

  Returns:
    An array specifying the insertion locations of `query` into `sorted_arr`.
  """
  sorted_arr, query = core.auto_insert_reshard(sorted_arr, query)
  out_dtype = dtypes._maybe_canonicalize_explicit_dtype(np.dtype(dtype), "searchsorted")
  prim = SearchSorted(
    core.typeof(sorted_arr),
    core.typeof(query),
    side=side,
    dimension=dimension,
    batch_dims=batch_dims,
    method=method,
    out_dtype=out_dtype,
  )
  return prim(sorted_arr, query)


def searchsorted(a: ArrayLike, v: ArrayLike, side: str = 'left',
                 sorter: ArrayLike | None = None, *, method: str = 'scan') -> Array:
  """Perform a binary search within a sorted array.

  JAX implementation of :func:`numpy.searchsorted`.

  This will return the indices within a sorted array ``a`` where values in ``v``
  can be inserted to maintain its sort order.

  Args:
    a: one-dimensional array, assumed to be in sorted order unless ``sorter`` is specified.
    v: N-dimensional array of query values
    side: ``'left'`` (default) or ``'right'``; specifies whether insertion indices will be
      to the left or the right in case of ties.
    sorter: optional array of indices specifying the sort order of ``a``. If specified,
      then the algorithm assumes that ``a[sorter]`` is in sorted order.
    method: one of ``'scan'`` (default), ``'scan_unrolled'``, ``'sort'`` or ``'compare_all'``.
      See *Note* below.

  Returns:
    Array of insertion indices of shape ``v.shape``.

  Note:
    The ``method`` argument controls the algorithm used to compute the insertion indices.

    - ``'scan'`` (the default) tends to be more performant on CPU, particularly when ``a`` is
      very large.
    - ``'scan_unrolled'`` is more performant on GPU at the expense of additional compile time.
    - ``'sort'`` is often more performant on accelerator backends like GPU and TPU, particularly
      when ``v`` is very large.
    - ``'compare_all'`` tends to be the most performant when ``a`` is very small.

  Examples:
    Searching for a single value:

    >>> a = jnp.array([1, 2, 2, 3, 4, 5, 5])
    >>> jnp.searchsorted(a, 2)
    Array(1, dtype=int32)
    >>> jnp.searchsorted(a, 2, side='right')
    Array(3, dtype=int32)

    Searching for a batch of values:

    >>> vals = jnp.array([0, 3, 8, 1.5, 2])
    >>> jnp.searchsorted(a, vals)
    Array([0, 3, 7, 1, 1], dtype=int32)

    Optionally, the ``sorter`` argument can be used to find insertion indices into
    an array sorted via :func:`jax.numpy.argsort`:

    >>> a = jnp.array([4, 3, 5, 1, 2])
    >>> sorter = jnp.argsort(a)
    >>> jnp.searchsorted(a, vals, sorter=sorter)
    Array([0, 2, 5, 1, 1], dtype=int32)

    The result is equivalent to passing the sorted array:

    >>> jnp.searchsorted(jnp.sort(a), vals)
    Array([0, 2, 5, 1, 1], dtype=int32)
  """
  if sorter is None:
    a, v = util.ensure_arraylike("searchsorted", a, v)
  else:
    a, v, sorter = util.ensure_arraylike("searchsorted", a, v, sorter)
  if a.ndim != 1:
    raise ValueError("a should be 1-dimensional")
  a, v = util.promote_dtypes(a, v)
  if sorter is not None:
    a = a[sorter]
  dtype = lax_utils.int_dtype_for_dim(a.shape[0], signed=True)

  # TODO(jakevdp): fix hijax primitive corner cases and use hijax.searchsorted direcly.
  return hijax.searchsorted_via_expand(a, v, side=side, method=method, dtype=dtype)

