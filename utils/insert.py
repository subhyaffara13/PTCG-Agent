
def insert(g: jit_utils.GraphContext, self, pos, tensor):
    return g.op("SequenceInsert", self, tensor, pos)


def insert(x, tck, m=1, per=0):
    # see the docstring of `_fitpack_py/insert`
    t, c, k = tck
    try:
        c[0][0]
        parametric = True
    except Exception:
        parametric = False
    if parametric:
        cc = []
        for c_vals in c:
            tt, cc_val, kk = insert(x, [t, c_vals, k], m)
            cc.append(cc_val)
        return (tt, cc, kk)
    else:
        tt, cc, ier = _fitpack.insert(per, t, c, k, x, m)
        if ier == 10:
            raise ValueError("Invalid input data")
        if ier:
            raise TypeError("An error occurred")
        return (tt, cc, k)


def insert(x, tck, m=1, per=0):
    """
    Insert knots into a B-spline.

    .. legacy:: function

        Specifically, we recommend constructing a `BSpline` object and using
        its ``insert_knot`` method.

    Given the knots and coefficients of a B-spline representation, create a
    new B-spline with a knot inserted `m` times at point `x`.
    This is a wrapper around the FORTRAN routine insert of FITPACK.

    Parameters
    ----------
    x : float
        A knot value at which to insert a new knot.  If `tck` was returned
        from ``splprep``, then the parameter values, u should be given.
    tck : a `BSpline` instance or a tuple
        If tuple, then it is expected to be a tuple (t,c,k) containing
        the vector of knots, the B-spline coefficients, and the degree of
        the spline.
    m : int, optional
        The number of times to insert the given knot (its multiplicity).
        Default is 1.
    per : int, optional
        If non-zero, the input spline is considered periodic.

    Returns
    -------
    BSpline instance or a tuple
        A new B-spline with knots t, coefficients c, and degree k.
        ``t(k+1) <= x <= t(n-k)``, where k is the degree of the spline.
        In case of a periodic spline (``per != 0``) there must be
        either at least k interior knots t(j) satisfying ``t(k+1)<t(j)<=x``
        or at least k interior knots t(j) satisfying ``x<=t(j)<t(n-k)``.
        A tuple is returned iff the input argument `tck` is a tuple, otherwise
        a BSpline object is constructed and returned.

    Notes
    -----
    Based on algorithms from [1]_ and [2]_.

    Manipulating the tck-tuples directly is not recommended. In new code,
    prefer using the `BSpline` objects, in particular `BSpline.insert_knot`
    method.

    See Also
    --------
    BSpline.insert_knot

    References
    ----------
    .. [1] W. Boehm, "Inserting new knots into b-spline curves.",
        Computer Aided Design, 12, p.199-201, 1980.
    .. [2] P. Dierckx, "Curve and surface fitting with splines, Monographs on
        Numerical Analysis", Oxford University Press, 1993.

    Examples
    --------
    You can insert knots into a B-spline.

    >>> from scipy.interpolate import splrep, insert
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 5)
    >>> y = np.sin(x)
    >>> tck = splrep(x, y)
    >>> tck[0]
    array([ 0.,  0.,  0.,  0.,  5., 10., 10., 10., 10.])

    A knot is inserted:

    >>> tck_inserted = insert(3, tck)
    >>> tck_inserted[0]
    array([ 0.,  0.,  0.,  0.,  3.,  5., 10., 10., 10., 10.])

    Some knots are inserted:

    >>> tck_inserted2 = insert(8, tck, m=3)
    >>> tck_inserted2[0]
    array([ 0.,  0.,  0.,  0.,  5.,  8.,  8.,  8., 10., 10., 10., 10.])

    """
    if isinstance(tck, BSpline):

        t, c, k = tck.tck

        # FITPACK expects the interpolation axis to be last, so roll it over
        # NB: if c array is 1D, transposes are no-ops
        sh = tuple(range(c.ndim))
        c = c.transpose(sh[1:] + (0,))
        t_, c_, k_ = _impl.insert(x, (t, c, k), m, per)

        # and roll the last axis back
        c_ = np.asarray(c_)
        c_ = c_.transpose((sh[-1],) + sh[:-1])
        return BSpline(t_, c_, k_)
    else:
        return _impl.insert(x, tck, m, per)


def insert(arr, obj, values, axis=None):
    """
    Insert values along the given axis before the given indices.

    Parameters
    ----------
    arr : array_like
        Input array.
    obj : slice, int, array-like of ints or bools
        Object that defines the index or indices before which `values` is
        inserted.

        .. versionchanged:: 2.1.2
            Boolean indices are now treated as a mask of elements to insert,
            rather than being cast to the integers 0 and 1.

        Support for multiple insertions when `obj` is a single scalar or a
        sequence with one element (similar to calling insert multiple
        times).
    values : array_like
        Values to insert into `arr`. If the type of `values` is different
        from that of `arr`, `values` is converted to the type of `arr`.
        `values` should be shaped so that ``arr[...,obj,...] = values``
        is legal.
    axis : int, optional
        Axis along which to insert `values`.  If `axis` is None then `arr`
        is flattened first.

    Returns
    -------
    out : ndarray
        A copy of `arr` with `values` inserted.  Note that `insert`
        does not occur in-place: a new array is returned. If
        `axis` is None, `out` is a flattened array.

    See Also
    --------
    append : Append elements at the end of an array.
    concatenate : Join a sequence of arrays along an existing axis.
    delete : Delete elements from an array.

    Notes
    -----
    Note that for higher dimensional inserts ``obj=0`` behaves very different
    from ``obj=[0]`` just like ``arr[:,0,:] = values`` is different from
    ``arr[:,[0],:] = values``. This is because of the difference between basic
    and advanced :ref:`indexing <basics.indexing>`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(6).reshape(3, 2)
    >>> a
    array([[0, 1],
           [2, 3],
           [4, 5]])
    >>> np.insert(a, 1, 6)
    array([0, 6, 1, 2, 3, 4, 5])
    >>> np.insert(a, 1, 6, axis=1)
    array([[0, 6, 1],
           [2, 6, 3],
           [4, 6, 5]])

    Difference between sequence and scalars,
    showing how ``obj=[1]`` behaves different from ``obj=1``:

    >>> np.insert(a, [1], [[7],[8],[9]], axis=1)
    array([[0, 7, 1],
           [2, 8, 3],
           [4, 9, 5]])
    >>> np.insert(a, 1, [[7],[8],[9]], axis=1)
    array([[0, 7, 8, 9, 1],
           [2, 7, 8, 9, 3],
           [4, 7, 8, 9, 5]])
    >>> np.array_equal(np.insert(a, 1, [7, 8, 9], axis=1),
    ...                np.insert(a, [1], [[7],[8],[9]], axis=1))
    True

    >>> b = a.flatten()
    >>> b
    array([0, 1, 2, 3, 4, 5])
    >>> np.insert(b, [2, 2], [6, 7])
    array([0, 1, 6, 7, 2, 3, 4, 5])

    >>> np.insert(b, slice(2, 4), [7, 8])
    array([0, 1, 7, 2, 8, 3, 4, 5])

    >>> np.insert(b, [2, 2], [7.13, False]) # type casting
    array([0, 1, 7, 0, 2, 3, 4, 5])

    >>> x = np.arange(8).reshape(2, 4)
    >>> idx = (1, 3)
    >>> np.insert(x, idx, 999, axis=1)
    array([[  0, 999,   1,   2, 999,   3],
           [  4, 999,   5,   6, 999,   7]])

    """
    conv = _array_converter(arr)
    arr, = conv.as_arrays(subok=False)

    ndim = arr.ndim
    arrorder = 'F' if arr.flags.fnc else 'C'
    if axis is None:
        if ndim != 1:
            arr = arr.ravel()
        # needed for np.matrix, which is still not 1d after being ravelled
        ndim = arr.ndim
        axis = ndim - 1
    else:
        axis = normalize_axis_index(axis, ndim)
    slobj = [slice(None)] * ndim
    N = arr.shape[axis]
    newshape = list(arr.shape)

    if isinstance(obj, slice):
        # turn it into a range object
        indices = arange(*obj.indices(N), dtype=intp)
    else:
        # need to copy obj, because indices will be changed in-place
        indices = np.array(obj)
        if indices.dtype == bool:
            if obj.ndim != 1:
                raise ValueError('boolean array argument obj to insert '
                                'must be one dimensional')
            indices = np.flatnonzero(obj)
        elif indices.ndim > 1:
            raise ValueError(
                "index array argument obj to insert must be one dimensional "
                "or scalar")
    if indices.size == 1:
        index = indices.item()
        if index < -N or index > N:
            raise IndexError(f"index {obj} is out of bounds for axis {axis} "
                             f"with size {N}")
        if (index < 0):
            index += N

        # There are some object array corner cases here, but we cannot avoid
        # that:
        values = array(values, copy=None, ndmin=arr.ndim, dtype=arr.dtype)
        if indices.ndim == 0:
            # broadcasting is very different here, since a[:,0,:] = ... behaves
            # very different from a[:,[0],:] = ...! This changes values so that
            # it works likes the second case. (here a[:,0:1,:])
            values = np.moveaxis(values, 0, axis)
        numnew = values.shape[axis]
        newshape[axis] += numnew
        new = empty(newshape, arr.dtype, arrorder)
        slobj[axis] = slice(None, index)
        new[tuple(slobj)] = arr[tuple(slobj)]
        slobj[axis] = slice(index, index + numnew)
        new[tuple(slobj)] = values
        slobj[axis] = slice(index + numnew, None)
        slobj2 = [slice(None)] * ndim
        slobj2[axis] = slice(index, None)
        new[tuple(slobj)] = arr[tuple(slobj2)]

        return conv.wrap(new, to_scalar=False)

    elif indices.size == 0 and not isinstance(obj, np.ndarray):
        # Can safely cast the empty list to intp
        indices = indices.astype(intp)

    indices[indices < 0] += N

    numnew = len(indices)
    order = indices.argsort(kind='mergesort')   # stable sort
    indices[order] += np.arange(numnew)

    newshape[axis] += numnew
    old_mask = ones(newshape[axis], dtype=bool)
    old_mask[indices] = False

    new = empty(newshape, arr.dtype, arrorder)
    slobj2 = [slice(None)] * ndim
    slobj[axis] = indices
    slobj2[axis] = old_mask
    new[tuple(slobj)] = values
    new[tuple(slobj2)] = arr

    return conv.wrap(new, to_scalar=False)


def insert(value_to_store: _ods_ir.Value, dest: _ods_ir.Value[_ods_ir.VectorType], dynamic_position: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], static_position: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return InsertOp(valueToStore=value_to_store, dest=dest, dynamic_position=dynamic_position, static_position=static_position, results=results, loc=loc, ip=ip).result


def insert(arr: ArrayLike, obj: ArrayLike | slice, values: ArrayLike,
           axis: int | None = None) -> Array:
  """Insert entries into an array at specified indices.

  JAX implementation of :func:`numpy.insert`.

  Args:
    arr: array object into which values will be inserted.
    obj: slice or array of indices specifying insertion locations.
    values: array of values to be inserted.
    axis: specify the insertion axis in the case of multi-dimensional
      arrays. If unspecified, ``arr`` will be flattened.

  Returns:
    A copy of ``arr`` with values inserted at the specified locations.

  See also:
    - :func:`jax.numpy.delete`: delete entries from an array.

  Examples:
    Inserting a single value:

    >>> x = jnp.arange(5)
    >>> jnp.insert(x, 2, 99)
    Array([ 0,  1, 99,  2,  3,  4], dtype=int32)

    Inserting multiple identical values using a slice:

    >>> jnp.insert(x, slice(None, None, 2), -1)
    Array([-1,  0,  1, -1,  2,  3, -1,  4], dtype=int32)

    Inserting multiple values using an index:

    >>> indices = jnp.array([4, 2, 5])
    >>> values = jnp.array([10, 11, 12])
    >>> jnp.insert(x, indices, values)
    Array([ 0,  1, 11,  2,  3, 10,  4, 12], dtype=int32)

    Inserting columns into a 2D array:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> indices = jnp.array([1, 3])
    >>> values = jnp.array([[10, 11],
    ...                     [12, 13]])
    >>> jnp.insert(x, indices, values, axis=1)
    Array([[ 1, 10,  2,  3, 11],
           [ 4, 12,  5,  6, 13]], dtype=int32)
  """
  a, _, values_arr = util.ensure_arraylike("insert", arr, 0 if isinstance(obj, slice) else obj, values)

  if axis is None:
    a = ravel(a)
    axis = 0
  axis = core.concrete_or_error(None, axis, "axis argument of jnp.insert()")
  axis = _canonicalize_axis(axis, a.ndim)
  if isinstance(obj, slice):
    indices = arange(*obj.indices(a.shape[axis]))
  else:
    indices = asarray(obj)

  if indices.ndim > 1:
    raise ValueError("jnp.insert(): obj must be a slice, a one-dimensional "
                     f"array, or a scalar; got {obj}")
  if not np.issubdtype(indices.dtype, np.integer):
    if indices.size == 0 and not isinstance(obj, Array):
      indices = indices.astype(int)
    else:
      # Note: np.insert allows boolean inputs but the behavior is deprecated.
      raise ValueError("jnp.insert(): index array must be "
                       f"integer typed; got {obj}")
  values_arr = array(values_arr, ndmin=a.ndim, dtype=a.dtype, copy=False)

  if indices.size == 1:
    index = ravel(indices)[0]
    if indices.ndim == 0:
      values_arr = moveaxis(values_arr, 0, axis)
    indices = array_creation.full(values_arr.shape[axis], index)
  n_input = a.shape[axis]
  n_insert = broadcast_shapes(indices.shape, (values_arr.shape[axis],))[0]
  out_shape = list(a.shape)
  out_shape[axis] += n_insert
  out = array_creation.zeros_like(a, shape=tuple(out_shape))

  indices = where(indices < 0, indices + n_input, indices)
  indices = clip(indices, 0, n_input)

  values_ind = indices.at[argsort(indices)].add(arange(n_insert, dtype=indices.dtype))
  arr_mask = array_creation.ones(n_input + n_insert, dtype=bool).at[values_ind].set(False)
  arr_ind = where(arr_mask, size=n_input)[0]

  out = out.at[(slice(None),) * axis + (values_ind,)].set(values_arr)
  out = out.at[(slice(None),) * axis + (arr_ind,)].set(a)

  return out


def insert(
    tree: tp.Any,
    extracted: list[tp.Any],
    is_leaf: tp.Callable[[tp.Any], bool] | None = None,
) -> tp.Any:
  if is_leaf is None:
    _is_leaf = lambda x: isinstance(x, ExtractIndex)
  else:
    _is_leaf = lambda x: isinstance(x, ExtractIndex) or is_leaf(x)

  def _leaf_fn(leaf: tp.Any):
    if isinstance(leaf, ExtractIndex):
      return extracted[leaf.index]
    return leaf

  return jax.tree.map(_leaf_fn, tree, is_leaf=_is_leaf)

