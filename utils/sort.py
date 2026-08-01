
def sort(
    config: Config,
    to_sort: Iterable[str],
    key: Callable[[str], Any] | None = None,
    reverse: bool = False,
) -> list[str]:
    return config.sorting_function(to_sort, key=key, reverse=reverse)


def sort(request):
    """
    Boolean 'sort' parameter.
    """
    return request.param


def sort(x, dim=-1, descending=False):
    return sort_stable(x, stable=False, dim=dim, descending=descending)


def sort(a: ArrayLike, axis=-1, kind=None, order: NotImplementedType = None):
    # `order` keyword arg is only relevant for structured dtypes; so not supported here.
    a, axis, stable = _sort_helper(a, axis, kind, order)
    result = torch.sort(a, dim=axis, stable=stable)
    return result.values


def sort(g: jit_utils.GraphContext, self, dim, descending, out=None):
    return symbolic_helper._sort_helper(g, self, dim, descending=descending, out=out)


def sort(g: jit_utils.GraphContext, self, dim, descending, out=None):
    return symbolic_helper._sort_helper(g, self, dim, descending=descending, out=out)


def sort(g: jit_utils.GraphContext, self, dim, descending, out=None):
    if out is not None:
        symbolic_helper._unimplemented(
            "Sort", "Out parameter is not supported for sort", self
        )
    self_sizes = symbolic_helper._get_tensor_sizes(self)
    try:
        dim_size = self_sizes[dim]
    except Exception:
        # FIXME(justinchuby): Avoid catching Exception.
        # Catch a more specific exception instead.
        dim_size = None

    if dim_size is None:
        return symbolic_helper._unimplemented("Sort", "input size not accessible", self)

    return g.op("TopK", self, k_i=dim_size, axis_i=dim, outputs=2)


def sort(key, new=new):
    """ Create a rule to sort by a key function.

    Examples
    ========

    >>> from sympy.strategies import sort
    >>> from sympy import Basic, S
    >>> sort_rl = sort(str)
    >>> sort_rl(Basic(S(3), S(1), S(2)))
    Basic(1, 2, 3)
    """

    def sort_rl(expr):
        return new(expr.__class__, *sorted(expr.args, key=key))
    return sort_rl


def sort(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    **kwargs: object,
) -> Array:
    # Note: this keyword argument is different, and the default is different.
    # We set it in kwargs like this because numpy.sort uses kind='quicksort'
    # as the default whereas cupy.sort uses kind=None.
    if stable:
        kwargs["kind"] = "stable"
    res = xp.sort(x, axis=axis, **kwargs)
    if descending:
        res = xp.flip(res, axis=axis)
    return res


def sort(
    x: Array,
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    **kwargs: object,
) -> Array:
    return torch.sort(x, dim=axis, descending=descending, stable=stable, **kwargs).values


def sort(
    x: Array,
    /,
    *,
    axis: int = -1,
    descending: py_bool = False,
    stable: py_bool = True,
) -> Array:
    """
    Array API compatibility layer around the lack of sort() in Dask.

    Warnings
    --------
    This function temporarily rechunks the array along `axis` to a single chunk.
    This can be extremely inefficient and can lead to out-of-memory errors.

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    x, restore = _ensure_single_chunk(x, axis)

    meta_xp = array_namespace(x._meta)
    x = da.map_blocks(
        meta_xp.sort,
        x,
        axis=axis,
        meta=x._meta,
        dtype=x.dtype,
        descending=descending,
        stable=stable,
    )

    return restore(x)


def sort(request):
    """
    Valid values for the 'sort' parameter used in the Index
    setops methods (intersection, union, etc.)

    Caution:
        Don't confuse this one with the "sort" fixture used
        for concat. That one has parameters [True, False].

        We can't combine them as sort=True is not permitted
        in the Index setops methods.
    """
    return request.param


def sort(a, axis=-1, kind=None, order=None, endwith=True, fill_value=None, *,
         stable=None, descending=None):
    """
    Return a sorted copy of the masked array.

    Equivalent to creating a copy of the array
    and applying the  MaskedArray ``sort()`` method.

    Refer to ``MaskedArray.sort`` for the full documentation

    See Also
    --------
    MaskedArray.sort : equivalent method

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = [11.2, -3.973, 0.801, -1.41]
    >>> mask = [0, 0, 0, 1]
    >>> masked_x = ma.masked_array(x, mask)
    >>> masked_x
    masked_array(data=[11.2, -3.973, 0.801, --],
                 mask=[False, False, False,  True],
           fill_value=1e+20)
    >>> ma.sort(masked_x)
    masked_array(data=[-3.973, 0.801, 11.2, --],
                 mask=[False, False, False,  True],
           fill_value=1e+20)
    """
    a = np.array(a, copy=True, subok=True)
    if axis is None:
        a = a.flatten()
        axis = 0

    if isinstance(a, MaskedArray):
        a.sort(axis=axis, kind=kind, order=order, endwith=endwith,
               fill_value=fill_value, stable=stable, descending=descending)
    else:
        a.sort(axis=axis, kind=kind, order=order, stable=stable, descending=descending)
    return a


def sort(a, axis=-1, kind=None, order=None, *, stable=None, descending=np._NoValue):
    """
    Return a sorted copy of an array.

    Parameters
    ----------
    a : array_like
        Array to be sorted.
    axis : int or None, optional
        Axis along which to sort. If None, the array is flattened before
        sorting. The default is -1, which sorts along the last axis.
    kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
        Sorting algorithm. The default is 'quicksort'. Note that both 'stable'
        and 'mergesort' use timsort or radix sort under the covers and,
        in general, the actual implementation will vary with data type.
        The 'mergesort' option is retained for backwards compatibility.
    order : str or list of str, optional
        When `a` is an array with fields defined, this argument specifies
        which fields to compare first, second, etc.  A single field can
        be specified as a string, and not all fields need be specified,
        but unspecified fields will still be used, in the order in which
        they come up in the dtype, to break ties.
    stable : bool, optional
        Sort stability. If ``True``, the returned array will maintain
        the relative order of ``a`` values which compare as equal.
        If ``False`` or ``None``, this is not guaranteed. Internally,
        this option selects ``kind='stable'``. Default: ``None``.

        .. versionadded:: 2.0.0
    descending : bool, optional
        Sort order. If ``True``, the returned array will be sorted in
        descending order. If ``False`` or ``None``, the returned array will
        be sorted in ascending order. Values that are NaN are sorted to the
        end for both orders. Default: ``None``.

        .. versionadded:: 2.5.0

    Returns
    -------
    sorted_array : ndarray
        Array of the same type and shape as `a`.

    See Also
    --------
    ndarray.sort : Method to sort an array in-place.
    argsort : Indirect sort.
    lexsort : Indirect stable sort on multiple keys.
    searchsorted : Find elements in a sorted array.
    partition : Partial sort.

    Notes
    -----
    The various sorting algorithms are characterized by their average speed,
    worst case performance, work space size, and whether they are stable. A
    stable sort keeps items with the same key in the same relative
    order. The four algorithms implemented in NumPy have the following
    properties:

    =========== ======= ============= ============ ========
       kind      speed   worst case    work space   stable
    =========== ======= ============= ============ ========
    'quicksort'    1     O(n^2)            0          no
    'heapsort'     3     O(n*log(n))       0          no
    'mergesort'    2     O(n*log(n))      ~n/2        yes
    'timsort'      2     O(n*log(n))      ~n/2        yes
    =========== ======= ============= ============ ========

    .. note:: The datatype determines which of 'mergesort' or 'timsort'
       is actually used, even if 'mergesort' is specified. User selection
       at a finer scale is not currently available.

    For performance, ``sort`` makes a temporary copy if needed to make the data
    `contiguous <https://numpy.org/doc/stable/glossary.html#term-contiguous>`_
    in memory along the sort axis. For even better performance and reduced
    memory consumption, ensure that the array is already contiguous along the
    sort axis.

    The sort order for complex numbers is lexicographic. If both the real
    and imaginary parts are non-nan then the order is determined by the
    real parts except when they are equal, in which case the order is
    determined by the imaginary parts.

    Previous to numpy 1.4.0 sorting real and complex arrays containing nan
    values led to undefined behaviour. In numpy versions >= 1.4.0 nan
    values are sorted to the end. The extended sort order is:

      * Real: [R, nan]
      * Complex: [R + Rj, R + nanj, nan + Rj, nan + nanj]

    where R is a non-nan real value. Complex values with the same nan
    placements are sorted according to the non-nan part if it exists.
    Non-nan values are sorted as before.

    quicksort has been changed to:
    `introsort <https://en.wikipedia.org/wiki/Introsort>`_.
    When sorting does not make enough progress it switches to
    `heapsort <https://en.wikipedia.org/wiki/Heapsort>`_.
    This implementation makes quicksort O(n*log(n)) in the worst case.

    'stable' automatically chooses the best stable sorting algorithm
    for the data type being sorted.
    It, along with 'mergesort' is currently mapped to
    `timsort <https://en.wikipedia.org/wiki/Timsort>`_
    or `radix sort <https://en.wikipedia.org/wiki/Radix_sort>`_
    depending on the data type.
    API forward compatibility currently limits the
    ability to select the implementation and it is hardwired for the different
    data types.

    Timsort is added for better performance on already or nearly
    sorted data. On random data timsort is almost identical to
    mergesort. It is now used for stable sort while quicksort is still the
    default sort if none is chosen. For timsort details, refer to
    `CPython listsort.txt
    <https://github.com/python/cpython/blob/3.7/Objects/listsort.txt>`_
    'mergesort' and 'stable' are mapped to radix sort for integer data types.
    Radix sort is an O(n) sort instead of O(n log n).

    NaT now sorts to the end of arrays for consistency with NaN.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1,4],[3,1]])
    >>> np.sort(a)                # sort along the last axis
    array([[1, 4],
           [1, 3]])
    >>> np.sort(a, axis=None)     # sort the flattened array
    array([1, 1, 3, 4])
    >>> np.sort(a, axis=0)        # sort along the first axis
    array([[1, 1],
           [3, 4]])

    Use the `order` keyword to specify a field to use when sorting a
    structured array:

    >>> dtype = [('name', 'S10'), ('height', float), ('age', int)]
    >>> values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),
    ...           ('Galahad', 1.7, 38)]
    >>> a = np.array(values, dtype=dtype)       # create a structured array
    >>> np.sort(a, order='height')                        # doctest: +SKIP
    array([('Galahad', 1.7, 38), ('Arthur', 1.8, 41),
           ('Lancelot', 1.8999999999999999, 38)],
          dtype=[('name', '|S10'), ('height', '<f8'), ('age', '<i4')])

    Sort by age, then height if ages are equal:

    >>> np.sort(a, order=['age', 'height'])               # doctest: +SKIP
    array([('Galahad', 1.7, 38), ('Lancelot', 1.8999999999999999, 38),
           ('Arthur', 1.8, 41)],
          dtype=[('name', '|S10'), ('height', '<f8'), ('age', '<i4')])

    """
    if axis is None:
        # flatten returns (1, N) for np.matrix, so always use the last axis
        a = asanyarray(a).flatten()
        axis = -1
    else:
        a = asanyarray(a).copy(order="K")
    # Sanitize for backward-compatibility
    if descending is not np._NoValue:
        a.sort(axis=axis, kind=kind, order=order, stable=stable, descending=descending)
    else:
        a.sort(axis=axis, kind=kind, order=order, stable=stable)
    return a


def sort(output_mask: _ods_ir.Type, sorted_keys: _ods_ir.Type, sorted_values: _ods_ir.Type, keys: _ods_ir.Value[_ods_ir.VectorType], values: _ods_ir.Value[_ods_ir.VectorType], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, descending: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return SortOp(output_mask=output_mask, sorted_keys=sorted_keys, sorted_values=sorted_values, keys=keys, values=values, mask=mask, descending=descending, loc=loc, ip=ip).results


def sort(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, dimension: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, is_stable: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, SortOp]:
  op = SortOp(result=result, inputs=inputs, dimension=dimension, is_stable=is_stable, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def sort(n: _ods_ir.Value[_ods_ir.IndexType], xy: _ods_ir.Value[_ods_ir.MemRefType], ys: _Sequence[_ods_ir.Value[_ods_ir.MemRefType]], perm_map: _Union[_ods_ir.AffineMap, _ods_ir.AffineMapAttr], algorithm: _Union[_Any, _ods_ir.Attribute], *, ny: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SortOp:
  return SortOp(n=n, xy=xy, ys=ys, perm_map=perm_map, algorithm=algorithm, ny=ny, loc=loc, ip=ip)


def sort(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, dimension: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, is_stable: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, SortOp]:
  op = SortOp(result=result, inputs=inputs, dimension=dimension, is_stable=is_stable, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def sort(operand: Array, dimension: int = -1,
         is_stable: bool = True, num_keys: int = 1) -> Array:
  ...


def sort(operand: Sequence[Array], dimension: int = -1,
         is_stable: bool = True, num_keys: int = 1) -> tuple[Array, ...]:
  ...


def sort(operand: Array | Sequence[Array], dimension: int = -1,
         is_stable: bool = True, num_keys: int = 1) -> Array | tuple[Array, ...]:
  """Wraps XLA's `Sort
  <https://www.openxla.org/xla/operation_semantics#sort>`_ operator.

  For floating point inputs, -0.0 and 0.0 are treated as equivalent, and NaN values
  are sorted to the end of the array. For complex inputs, the sort order is
  lexicographic over the real and imaginary parts, with the real part primary.

  Args:
    operand : Array or sequence of arrays
    dimension : integer dimension along which to sort. Default: -1.
    is_stable : boolean specifying whether to use a stable sort. Default: True.
    num_keys : number of operands to treat as sort keys. Default: 1.
      For num_keys > 1, the sort order will be determined lexicographically using
      the first `num_keys` arrays, with the first key being primary.
      The remaining operands will be returned with the same permutation.

  Returns:
    operand : sorted version of the input or inputs.
  """
  if isinstance(operand, Sequence):
    if len(operand) == 0:
      raise TypeError("Sort requires at least one operand")
    if not (1 <= num_keys <= len(operand)):
      raise ValueError(f"{num_keys=} must be between 1 and {len(operand)=}")
    dimension = canonicalize_axis(dimension, len(operand[0].shape))
    operand = core.auto_insert_reshard(*operand)
    return tuple(sort_p.bind(*operand, dimension=dimension,
                             is_stable=is_stable, num_keys=num_keys))
  else:
    if num_keys != 1:
      raise ValueError(f"{num_keys=} must equal 1 for a single operand.")
    dimension = canonicalize_axis(dimension, len(operand.shape))
    return sort_p.bind(operand, dimension=dimension, is_stable=is_stable,
                       num_keys=1)[0]


def sort(
    a: ArrayLike,
    axis: int | None = -1,
    *,
    kind: None = None,
    order: None = None,
    stable: bool = True,
    descending: bool = False,
) -> Array:
  """Return a sorted copy of an array.

  JAX implementation of :func:`numpy.sort`.

  Args:
    a: array to sort
    axis: integer axis along which to sort. Defaults to ``-1``, i.e. the last
      axis. If ``None``, then ``a`` is flattened before being sorted.
    stable: boolean specifying whether a stable sort should be used. Default=True.
    descending: boolean specifying whether to sort in descending order. Default=False.
    kind: deprecated; instead specify sort algorithm using stable=True or stable=False.
    order: not supported by JAX

  Returns:
    Sorted array of shape ``a.shape`` (if ``axis`` is an integer) or of shape
    ``(a.size,)`` (if ``axis`` is None).

  Examples:
    Simple 1-dimensional sort

    >>> x = jnp.array([1, 3, 5, 4, 2, 1])
    >>> jnp.sort(x)
    Array([1, 1, 2, 3, 4, 5], dtype=int32)

    Sort along the last axis of an array:

    >>> x = jnp.array([[2, 1, 3],
    ...                [4, 3, 6]])
    >>> jnp.sort(x, axis=1)
    Array([[1, 2, 3],
           [3, 4, 6]], dtype=int32)

  See also:
    - :func:`jax.numpy.argsort`: return indices of sorted values.
    - :func:`jax.numpy.lexsort`: lexicographical sort of multiple arrays.
    - :func:`jax.lax.sort`: lower-level function wrapping XLA's Sort operator.
  """
  arr = util.ensure_arraylike("sort", a)
  if kind is not None:
    raise TypeError("'kind' argument to sort is not supported. Use"
                    " stable=True or stable=False to specify sort stability.")
  if order is not None:
    raise TypeError("'order' argument to sort is not supported.")
  if axis is None:
    arr = arr.ravel()
    axis = 0
  dimension = canonicalize_axis(axis, arr.ndim)
  result = lax.sort(arr, dimension=dimension, is_stable=stable)
  return lax.rev(result, dimensions=[dimension]) if descending else result

