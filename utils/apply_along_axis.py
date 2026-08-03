from typing import Callable

def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    """
    Apply a function to 1-D slices along the given axis.

    Execute `func1d(a, *args, **kwargs)` where `func1d` operates on 1-D arrays
    and `a` is a 1-D slice of `arr` along `axis`.

    This is equivalent to (but faster than) the following use of `ndindex` and
    `s_`, which sets each of ``ii``, ``jj``, and ``kk`` to a tuple of indices::

        Ni, Nk = a.shape[:axis], a.shape[axis+1:]
        for ii in ndindex(Ni):
            for kk in ndindex(Nk):
                f = func1d(arr[ii + s_[:,] + kk])
                Nj = f.shape
                for jj in ndindex(Nj):
                    out[ii + jj + kk] = f[jj]

    Equivalently, eliminating the inner loop, this can be expressed as::

        Ni, Nk = a.shape[:axis], a.shape[axis+1:]
        for ii in ndindex(Ni):
            for kk in ndindex(Nk):
                out[ii + s_[...,] + kk] = func1d(arr[ii + s_[:,] + kk])

    Parameters
    ----------
    func1d : function (M,) -> (Nj...)
        This function should accept 1-D arrays. It is applied to 1-D
        slices of `arr` along the specified axis.
    axis : integer
        Axis along which `arr` is sliced.
    arr : ndarray (Ni..., M, Nk...)
        Input array.
    args : any
        Additional arguments to `func1d`.
    kwargs : any
        Additional named arguments to `func1d`.

    Returns
    -------
    out : ndarray  (Ni..., Nj..., Nk...)
        The output array. The shape of `out` is identical to the shape of
        `arr`, except along the `axis` dimension. This axis is removed, and
        replaced with new dimensions equal to the shape of the return value
        of `func1d`. So if `func1d` returns a scalar `out` will have one
        fewer dimensions than `arr`.

    See Also
    --------
    apply_over_axes : Apply a function repeatedly over multiple axes.

    Examples
    --------
    >>> import numpy as np
    >>> def my_func(a):
    ...     \"\"\"Average first and last element of a 1-D array\"\"\"
    ...     return (a[0] + a[-1]) * 0.5
    >>> b = np.array([[1,2,3], [4,5,6], [7,8,9]])
    >>> np.apply_along_axis(my_func, 0, b)
    array([4., 5., 6.])
    >>> np.apply_along_axis(my_func, 1, b)
    array([2.,  5.,  8.])

    For a function that returns a 1D array, the number of dimensions in
    `outarr` is the same as `arr`.

    >>> b = np.array([[8,1,7], [4,3,9], [5,2,6]])
    >>> np.apply_along_axis(sorted, 1, b)
    array([[1, 7, 8],
           [3, 4, 9],
           [2, 5, 6]])

    For a function that returns a higher dimensional array, those dimensions
    are inserted in place of the `axis` dimension.

    >>> b = np.array([[1,2,3], [4,5,6], [7,8,9]])
    >>> np.apply_along_axis(np.diag, -1, b)
    array([[[1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]],
           [[4, 0, 0],
            [0, 5, 0],
            [0, 0, 6]],
           [[7, 0, 0],
            [0, 8, 0],
            [0, 0, 9]]])
    """
    # handle negative axes
    conv = _array_converter(arr)
    arr = conv[0]

    nd = arr.ndim
    axis = normalize_axis_index(axis, nd)

    # arr, with the iteration axis at the end
    in_dims = list(range(nd))
    inarr_view = transpose(arr, in_dims[:axis] + in_dims[axis + 1:] + [axis])

    # compute indices for the iteration axes, and append a trailing ellipsis to
    # prevent 0d arrays decaying to scalars, which fixes gh-8642
    inds = ndindex(inarr_view.shape[:-1])
    inds = (ind + (Ellipsis,) for ind in inds)

    # invoke the function on the first item
    try:
        ind0 = next(inds)
    except StopIteration:
        raise ValueError(
            'Cannot apply_along_axis when any iteration dimensions are 0'
        ) from None
    res = asanyarray(func1d(inarr_view[ind0], *args, **kwargs))

    # build a buffer for storing evaluations of func1d.
    # remove the requested axis, and add the new ones on the end.
    # laid out so that each write is contiguous.
    # for a tuple index inds, buff[inds] = func1d(inarr_view[inds])
    if not isinstance(res, matrix):
        buff = zeros_like(res, shape=inarr_view.shape[:-1] + res.shape)
    else:
        # Matrices are nasty with reshaping, so do not preserve them here.
        buff = zeros(inarr_view.shape[:-1] + res.shape, dtype=res.dtype)

    # permutation of axes such that out = buff.transpose(buff_permute)
    buff_dims = list(range(buff.ndim))
    buff_permute = (
        buff_dims[0 : axis] +
        buff_dims[buff.ndim - res.ndim : buff.ndim] +
        buff_dims[axis : buff.ndim - res.ndim]
    )

    # save the first result, then compute and save all remaining results
    buff[ind0] = res
    for ind in inds:
        buff[ind] = asanyarray(func1d(inarr_view[ind], *args, **kwargs))

    res = transpose(buff, buff_permute)
    return conv.wrap(res)


def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    """
    (This docstring should be overwritten)
    """
    arr = array(arr, copy=False, subok=True)
    nd = arr.ndim
    axis = normalize_axis_index(axis, nd)
    ind = [0] * (nd - 1)
    i = np.zeros(nd, 'O')
    indlist = list(range(nd))
    indlist.remove(axis)
    i[axis] = slice(None, None)
    outshape = np.asarray(arr.shape).take(indlist)
    i.put(indlist, ind)
    res = func1d(arr[tuple(i.tolist())], *args, **kwargs)
    #  if res is a number, then we have a smaller output array
    asscalar = np.isscalar(res)
    if not asscalar:
        try:
            len(res)
        except TypeError:
            asscalar = True
    # Note: we shouldn't set the dtype of the output from the first result
    # so we force the type to object, and build a list of dtypes.  We'll
    # just take the largest, to avoid some downcasting
    dtypes = []
    if asscalar:
        dtypes.append(np.asarray(res).dtype)
        outarr = zeros(outshape, object)
        outarr[tuple(ind)] = res
        Ntot = np.prod(outshape)
        k = 1
        while k < Ntot:
            # increment the index
            ind[-1] += 1
            n = -1
            while (ind[n] >= outshape[n]) and (n > (1 - nd)):
                ind[n - 1] += 1
                ind[n] = 0
                n -= 1
            i.put(indlist, ind)
            res = func1d(arr[tuple(i.tolist())], *args, **kwargs)
            outarr[tuple(ind)] = res
            dtypes.append(asarray(res).dtype)
            k += 1
    else:
        res = array(res, copy=False, subok=True)
        j = i.copy()
        j[axis] = ([slice(None, None)] * res.ndim)
        j.put(indlist, ind)
        Ntot = np.prod(outshape)
        holdshape = outshape
        outshape = list(arr.shape)
        outshape[axis] = res.shape
        dtypes.append(asarray(res).dtype)
        outshape = flatten_inplace(outshape)
        outarr = zeros(outshape, object)
        outarr[tuple(flatten_inplace(j.tolist()))] = res
        k = 1
        while k < Ntot:
            # increment the index
            ind[-1] += 1
            n = -1
            while (ind[n] >= holdshape[n]) and (n > (1 - nd)):
                ind[n - 1] += 1
                ind[n] = 0
                n -= 1
            i.put(indlist, ind)
            j.put(indlist, ind)
            res = func1d(arr[tuple(i.tolist())], *args, **kwargs)
            outarr[tuple(flatten_inplace(j.tolist()))] = res
            dtypes.append(asarray(res).dtype)
            k += 1
    max_dtypes = np.dtype(np.asarray(dtypes).max())
    if not hasattr(arr, '_mask'):
        result = np.asarray(outarr, dtype=max_dtypes)
    else:
        result = asarray(outarr, dtype=max_dtypes)
        result.fill_value = ma.default_fill_value(result)
    return result


def apply_along_axis(
    func1d: Callable, axis: int, arr: ArrayLike, *args, **kwargs
) -> Array:
  """Apply a function to 1D array slices along an axis.

  JAX implementation of :func:`numpy.apply_along_axis`. While NumPy implements
  this iteratively, JAX implements this via :func:`jax.vmap`, and so ``func1d``
  must be compatible with ``vmap``.

  Args:
    func1d: a callable function with signature ``func1d(arr, /, *args, **kwargs)``
      where ``*args`` and ``**kwargs`` are the additional positional and keyword
      arguments passed to :func:`apply_along_axis`.
    axis: integer axis along which to apply the function.
    arr: the array over which to apply the function.
    args, kwargs: additional positional and keyword arguments are passed through
      to ``func1d``.

  Returns:
    The result of ``func1d`` applied along the specified axis.

  See also:
    - :func:`jax.vmap`: a more direct way to create a vectorized version of a function.
    - :func:`jax.numpy.apply_over_axes`: repeatedly apply a function over multiple axes.
    - :func:`jax.numpy.vectorize`: create a vectorized version of a function.

  Examples:
    A simple example in two dimensions, where the function is applied either row-wise
    or column-wise:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> def func1d(x):
    ...   return jnp.sum(x ** 2)
    >>> jnp.apply_along_axis(func1d, 0, x)
    Array([17, 29, 45], dtype=int32)
    >>> jnp.apply_along_axis(func1d, 1, x)
    Array([14, 77], dtype=int32)

    For 2D inputs, this can be equivalently expressed using :func:`jax.vmap`,
    though note that `vmap` specifies the mapped axis rather than the applied axis:

    >>> jax.vmap(func1d, in_axes=1)(x)  # same as applying along axis 0
    Array([17, 29, 45], dtype=int32)
    >>> jax.vmap(func1d, in_axes=0)(x)  # same as applying along axis 1
    Array([14, 77], dtype=int32)

    For 3D inputs, :func:`apply_along_axis` is equivalent to mapping over two
    dimensions:

    >>> x_3d = jnp.arange(24).reshape(2, 3, 4)
    >>> jnp.apply_along_axis(func1d, 2, x_3d)
    Array([[  14,  126,  366],
           [ 734, 1230, 1854]], dtype=int32)
    >>> jax.vmap(jax.vmap(func1d))(x_3d)
    Array([[  14,  126,  366],
           [ 734, 1230, 1854]], dtype=int32)

    The applied function may also take arbitrary positional or keyword arguments,
    which should be passed directly as additional arguments to :func:`apply_along_axis`:

    >>> def func1d(x, exponent):
    ...   return jnp.sum(x ** exponent)
    >>> jnp.apply_along_axis(func1d, 0, x, exponent=3)
    Array([ 65, 133, 243], dtype=int32)
  """
  util.check_arraylike("apply_along_axis", arr)
  num_dims = np.ndim(arr)
  axis = _canonicalize_axis(axis, num_dims)
  func = lambda arr: func1d(arr, *args, **kwargs)
  for i in range(1, num_dims - axis):
    func = api.vmap(func, in_axes=i, out_axes=-1)
  for i in range(axis):
    func = api.vmap(func, in_axes=0, out_axes=0)
  return func(arr)

