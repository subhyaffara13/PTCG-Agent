
def mean(
    input: Tensor | MaskedTensor,
    dim: DimOrDims = None,
    *,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

By definition, the identity value of a mean operation is the mean
value of the tensor. If all elements of the input tensor along given
dimension(s) :attr:`dim` are masked-out, the identity value of the
mean is undefined.  Due to this ambiguity, the elements of output
tensor with strided layout, that correspond to fully masked-out
elements, have ``nan`` values.

{reduction_args}

{reduction_example}"""
    dtype_source = "Optional"
    if dtype is None:
        dtype = input.dtype
        dtype_source = "Input"

    if not (dtype.is_floating_point or dtype.is_complex):
        raise ValueError(
            f"mean(): Could not infer output dtype. {dtype_source} dtype must be either "
            f"a floating point or complex dtype. Got: {dtype}"
        )
    if input.layout == torch.strided:
        if mask is None:
            # TODO: compute count analytically
            # pyrefly: ignore [no-matching-overload]
            count = sum(
                torch.ones(input.shape, dtype=torch.int64, device=input.device),
                dim,
                keepdim=keepdim,
            )
            # pyrefly: ignore [no-matching-overload]
            total = sum(input, dim, keepdim=keepdim, dtype=dtype)
        else:
            inmask = _input_mask(input, mask=mask)
            count = inmask.sum(dim=dim, keepdim=bool(keepdim))
            # pyrefly: ignore [no-matching-overload]
            total = sum(input, dim, keepdim=keepdim, dtype=dtype, mask=inmask)
        return total / count
    elif input.layout == torch.sparse_csr:
        mask_input = _combine_input_and_mask(mean, input, mask)
        dim_ = _canonical_dim(dim, mask_input.ndim)
        if mask is None:
            raise ValueError(
                "masked mean expects explicit mask for sparse_csr tensor input"
            )
        return _sparse_csr_segment_reduction_helper(
            torch.mean, mask_input, dim_, bool(keepdim), dtype
        )
    else:
        raise ValueError(
            f"masked mean expects strided or sparse_csr tensor (got {input.layout} tensor)"
        )


def mean(x, axis=None, keepdim=False, *, dtype=None):
    if dtype is not None:
        x = to_dtype(x, dtype)
    size = x.get_size()
    axis = _validate_reduction_axis(x, axis)
    # compute in higher-precision until end of mean lowering
    output_dtype = x.get_dtype()
    if output_dtype in (torch.float16, torch.bfloat16):
        x = to_dtype(x, torch.float)
    sum_result = sum_(x, axis, keepdim)
    denom = sympy_product(size[i] for i in axis)
    denom = ir.IndexingConstant(index=denom, dtype=x.get_dtype(), device=x.get_device())
    denom = ExpandView.create(denom, list(sum_result.get_size()))
    return to_dtype(div(sum_result, denom), output_dtype)


def mean(
    a: ArrayLike,
    axis: AxisLike = None,
    dtype: DTypeLike | None = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    dtype = _atleast_float(dtype, a.dtype)

    axis_kw = {} if axis is None else {"dim": axis}
    result = a.mean(dtype=dtype, **axis_kw)

    return result


def mean(
    a: TensorLikeType,
    dim: DimsType | None = None,
    keepdim: bool = False,
    *,
    dtype=None,
    out=None,
) -> TensorLikeType:
    # reduces over all dimensions if dim=() is passed
    if dim == () or dim == []:
        dim = None
    orig_dtype = dtype
    if dtype is None:
        dtype = a.dtype
    result = _reduction(
        a,
        prims.sum,
        dims=dim,
        keepdims=keepdim,
        dtype=dtype,
        out=None,
        output_dtype_kind=REDUCTION_OUTPUT_TYPE_KIND.KEEP_PROMOTED_TYPE,
    )
    torch._check(
        utils.is_float_dtype(dtype) or utils.is_complex_dtype(dtype),
        lambda: (
            f"mean(): could not infer output dtype. "
            f"{'Input' if orig_dtype is None else 'Optional'} dtype must be either "
            f"a floating point or complex dtype. Got: {dtype}"
        ),
    )
    if isinstance(dim, Dim):
        dim = (dim,)  # type: ignore[assignment]
    dims = utils.reduction_dims(a.shape, dim)  # type: ignore[arg-type]
    nelem = 1 if a.ndim == 0 else reduce(operator.mul, (a.shape[i] for i in dims), 1)
    result = true_divide(result, nelem)
    result_dtype = a.dtype if dtype is None else dtype
    result = _maybe_convert_to_dtype(result, result_dtype)  # type: ignore[method-assign]
    if out is not None:
        if not isinstance(out, TensorLike):
            raise AssertionError(f"out must be TensorLike, got {type(out)}")
        out = _maybe_resize_out(out, result.shape)
        return _safe_copy_out(copy_from=result, copy_to=out)  # type: ignore[arg-type]
    return result


def mean(input, labels=None, index=None):
    """
    Calculate the mean of the values of an array at labels.

    Parameters
    ----------
    input : array_like
        Array on which to compute the mean of elements over distinct
        regions.
    labels : array_like, optional
        Array of labels of same shape, or broadcastable to the same shape as
        `input`. All elements sharing the same label form one region over
        which the mean of the elements is computed.
    index : int or sequence of ints, optional
        Labels of the objects over which the mean is to be computed.
        Default is None, in which case the mean for all values where label is
        greater than 0 is calculated.

    Returns
    -------
    out : list
        Sequence of same length as `index`, with the mean of the different
        regions labeled by the labels in `index`.

    See Also
    --------
    variance, standard_deviation, minimum, maximum, sum, label

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.arange(25).reshape((5,5))
    >>> labels = np.zeros_like(a)
    >>> labels[3:5,3:5] = 1
    >>> index = np.unique(labels)
    >>> labels
    array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 1, 1],
           [0, 0, 0, 1, 1]])
    >>> index
    array([0, 1])
    >>> ndimage.mean(a, labels=labels, index=index)
    [10.285714285714286, 21.0]

    """

    count, sum = _stats(input, labels, index)
    return sum / np.asanyarray(count).astype(np.float64)


def mean(
    x: Array,
    /,
    *,
    axis: int | tuple[int, ...] | None = None,
    keepdims: bool = False,
    xp: ModuleType | None = None,
) -> Array:  # numpydoc ignore=PR01,RT01
    """
    Complex mean, https://github.com/data-apis/array-api/issues/846.
    """
    if xp is None:
        xp = array_namespace(x)

    if xp.isdtype(x.dtype, "complex floating"):
        x_real = xp.real(x)
        x_imag = xp.imag(x)
        mean_real = xp.mean(x_real, axis=axis, keepdims=keepdims)
        mean_imag = xp.mean(x_imag, axis=axis, keepdims=keepdims)
        return mean_real + (mean_imag * xp.asarray(1j))
    return xp.mean(x, axis=axis, keepdims=keepdims)


def mean(x: Array,
         /,
         *,
         axis: int | tuple[int, ...] | None = None,
         keepdims: bool = False,
         **kwargs: object) -> Array:
    # https://github.com/pytorch/pytorch/issues/29137
    if axis == ():
        return torch.clone(x)
    if axis is None:
        # torch doesn't support keepdims with axis=None
        # (https://github.com/pytorch/pytorch/issues/71209)
        res = torch.mean(x, **kwargs)
        res = _axis_none_keepdims(res, x.ndim, keepdims)
        return res
    return torch.mean(x, axis, keepdims=keepdims, **kwargs)


def mean(
    matrix: Array,
    weights: ArrayLike | None = None,
    axis: None | int | tuple[int, ...] = None
) -> Array:
    xp = array_namespace(matrix)
    if matrix.shape[0] == 0:
        raise ValueError("Mean of an empty rotation set is undefined.")
    # Axis logic: For None, we reduce over all axes. For int, we only reduce over that
    # axis. For tuple, we reduce over all specified axes.
    all_axes = tuple(range(matrix.ndim - 2))
    if axis is None:
        axis = all_axes
    elif isinstance(axis, int):
        axis = (axis,)
    if not isinstance(axis, tuple):
        raise ValueError("`axis` must be None, int, or tuple of ints.")
    # Ensure all axes are within bounds
    if (axis != () and
       (min(axis) < -(matrix.ndim - 2) or max(axis) > (matrix.ndim - 3))
    ):
        raise ValueError(
            f"axis {axis} is out of bounds for transform with shape "
            f"{matrix.shape[:-2]}."
        )
    # Ensure all axes are positive and unique
    axis = tuple(sorted(set(x % (matrix.ndim - 2) for x in axis)))

    lazy = is_lazy_array(matrix)
    quats = quat_from_matrix_orthogonal(matrix[..., :3, :3])
    if weights is None:
        quats_mean = quat_mean(quats, axis=axis)
    else:
        neg_weights = weights < 0  # type:ignore[operator]
        any_neg_weights = xp.any(neg_weights)
        if not lazy and any_neg_weights:
            raise ValueError("`weights` must be non-negative.")
        if weights.shape != matrix.shape[:-2]:  # type:ignore[union-attr]
            raise ValueError(
                f"Expected `weights` to match transform shape, got shape "
                f"{weights.shape} for {matrix.shape[:-2]} transformations."  # type:ignore[union-attr]
            )
        quats_mean = quat_mean(quats, weights=weights, axis=axis)
    r_mean = quat_as_matrix(quats_mean)

    t = matrix[..., :3, 3]
    if weights is None:
        t_mean = xp.mean(t, axis=axis)
    else:
        norm = xp.sum(weights[..., None], axis=axis)  # type:ignore[index]
        wsum = xp.sum(t * weights[..., None], axis=axis)  # type:ignore[index]
        t_mean = wsum / norm

    tf = _create_transformation_matrix(t_mean, r_mean)
    if weights is not None and lazy:
        # We cannot raise on negative weights because jit code needs to be
        # non-branching. We return NaN instead
        mask = xp.where(any_neg_weights, xp.nan, 1.0)  # pyrefly:ignore[unbound-name]
        tf = mask * tf
    return tf


def mean(
    quat: Array,
    weights: ArrayLike | None = None,
    axis: None | int | tuple[int, ...] = None,
) -> Array:
    xp = array_namespace(quat)
    device = xp_device(quat)
    dtype = xp_result_type(quat, force_floating=True, xp=xp)
    if quat.shape[0] == 0:
        raise ValueError("Mean of an empty rotation set is undefined.")
    # Axis logic: For None, we reduce over all axes. For int, we only reduce over that
    # axis. For tuple, we reduce over all specified axes.
    all_axes = tuple(range(quat.ndim - 1))
    if axis is None:
        axis = all_axes
    elif isinstance(axis, int):
        axis = (axis,)
    if not isinstance(axis, tuple):
        raise ValueError("`axis` must be None, int, or tuple of ints.")
    # Ensure all axes are within bounds
    if axis != () and (min(axis) < -(quat.ndim - 1) or max(axis) > (quat.ndim - 2)):
        raise ValueError(
            f"axis {axis} is out of bounds for rotation with shape {quat.shape[:-1]}."
        )
    # Ensure all axes are positive and unique
    axis = tuple(sorted(set(x % (quat.ndim - 1) for x in axis)))

    lazy = is_lazy_array(quat)
    # Branching code is okay for checks that include meta info such as shapes and types
    quat_expand = quat[..., None, :]
    if weights is None:
        K = xp.matrix_transpose(quat_expand) @ quat_expand
    else:
        weights = xp.asarray(weights, dtype=dtype, device=device)
        neg_weights = weights < 0
        if not lazy and xp.any(neg_weights):
            raise ValueError("`weights` must be non-negative.")
        elif lazy:
            # We cannot check for negative weights because jit code needs to be
            # non-branching. We return NaN instead
            weights = xp.where(neg_weights, xp.nan, weights)

        if not broadcastable(quat.shape[:-1], weights.shape):
            raise ValueError(
                "Expected `weights` to be broadcastable to rotation shape, got shape "
                f"{weights.shape} for {quat.shape[:-1]} rotations."
            )

        # Make sure we can transpose quat
        weighted_quat = weights[..., None, None] * quat_expand
        K = xp.matrix_transpose(weighted_quat) @ quat_expand

    # Move reduction axes to the end
    keep_axes = tuple(i for i in all_axes if i not in axis)
    axes_order = keep_axes + axis
    K_reordered = xp.moveaxis(K, axes_order, all_axes)
    # Reshape to flatten reduction axes
    new_shape = K_reordered.shape[: len(keep_axes)] + (-1, 4, 4)
    K = xp.mean(xp.reshape(K_reordered, new_shape), axis=-3)
    _, v = xp.linalg.eigh(K)
    return v[..., -1]


def mean(
    values: np.ndarray,
    mask: npt.NDArray[np.bool_],
    *,
    skipna: bool = True,
    axis: AxisInt | None = None,
):
    if not values.size or mask.all():
        return libmissing.NA
    return _reductions(np.mean, values=values, mask=mask, skipna=skipna, axis=axis)


def mean(a, axis=None, dtype=None, out=None, keepdims=np._NoValue, *,
         where=np._NoValue):
    """
    Compute the arithmetic mean along the specified axis.

    Returns the average of the array elements.  The average is taken over
    the flattened array by default, otherwise over the specified axis.
    `float64` intermediate and return values are used for integer inputs.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose mean is desired. If `a` is not an
        array, a conversion is attempted.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the means are computed. The default is to
        compute the mean of the flattened array.

        If this is a tuple of ints, a mean is performed over multiple axes,
        instead of a single axis or all the axes as before.
    dtype : data-type, optional
        Type to use in computing the mean.  For integer inputs, the default
        is `float64`; for floating point inputs, it is the same as the
        input dtype.
    out : ndarray, optional
        Alternate output array in which to place the result.  The default
        is ``None``; if provided, it must have the same shape as the
        expected output, but the type will be cast if necessary.
        See :ref:`ufuncs-output-type` for more details.
        See :ref:`ufuncs-output-type` for more details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `mean` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    where : array_like of bool, optional
        Elements to include in the mean. See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.20.0

    Returns
    -------
    m : ndarray, see dtype parameter above
        If `out=None`, returns a new array containing the mean values,
        otherwise a reference to the output array is returned.

    See Also
    --------
    average : Weighted average
    std, var, nanmean, nanstd, nanvar

    Notes
    -----
    The arithmetic mean is the sum of the elements along the axis divided
    by the number of elements.

    Note that for floating-point input, the mean is computed using the
    same precision the input has.  Depending on the input data, this can
    cause the results to be inaccurate, especially for `float32` (see
    example below).  Specifying a higher-precision accumulator using the
    `dtype` keyword can alleviate this issue.

    By default, `float16` results are computed using `float32` intermediates
    for extra precision.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.mean(a)
    2.5
    >>> np.mean(a, axis=0)
    array([2., 3.])
    >>> np.mean(a, axis=1)
    array([1.5, 3.5])

    In single precision, `mean` can be inaccurate:

    >>> a = np.zeros((2, 512*512), dtype=np.float32)
    >>> a[0, :] = 1.0
    >>> a[1, :] = 0.1
    >>> np.mean(a)
    np.float32(0.54999924)

    Computing the mean in float64 is more accurate:

    >>> np.mean(a, dtype=np.float64)
    0.55000000074505806 # may vary

    Computing the mean in timedelta64 is available:

    >>> b = np.array([1, 3], dtype="timedelta64[D]")
    >>> np.mean(b)
    np.timedelta64(2,'D')

    Specifying a where argument:

    >>> a = np.array([[5, 9, 13], [14, 10, 12], [11, 15, 19]])
    >>> np.mean(a)
    12.0
    >>> np.mean(a, where=[[True], [False], [False]])
    9.0

    """
    kwargs = {}
    if keepdims is not np._NoValue:
        kwargs['keepdims'] = keepdims
    if where is not np._NoValue:
        kwargs['where'] = where
    if type(a) is not mu.ndarray:
        try:
            mean = a.mean
        except AttributeError:
            pass
        else:
            return mean(axis=axis, dtype=dtype, out=out, **kwargs)

    return _methods._mean(a, axis=axis, dtype=dtype,
                          out=out, **kwargs)


def mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False, *,
         where: ArrayLike | None = None) -> Array:
  r"""Return the mean of array elements along a given axis.

  JAX implementation of :func:`numpy.mean`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      mean to be computed. If None, mean is computed along all the axes.
    dtype: The type of the output array. If None (default) then the output dtype
      will be match the input dtype for floating point inputs, or be set to float32
      or float64 for non-floating-point inputs.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      mean. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array of the mean along the given axis.

  Notes:
    For inputs of type `float16` or `bfloat16`, the reductions will be performed at
    float32 precision.

  See also:
    - :func:`jax.numpy.average`: Compute the weighted average of array elements
    - :func:`jax.numpy.sum`: Compute the sum of array elements.

  Examples:
    By default, the mean is computed along all the axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 6, 3],
    ...                [8, 1, 2, 9]])
    >>> jnp.mean(x)
    Array(3.8333335, dtype=float32)

    If ``axis=1``, the mean is computed along axis 1.

    >>> jnp.mean(x, axis=1)
    Array([2.5, 4. , 5. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.mean(x, axis=1, keepdims=True)
    Array([[2.5],
           [4. ],
           [5. ]], dtype=float32)

    To use only specific elements of ``x`` to compute the mean, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 0, 1],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.mean(x, axis=1, keepdims=True, where=where)
    Array([[2.5],
           [2.5],
           [6. ]], dtype=float32)
  """
  return _mean(a, _ensure_optional_axes(axis), dtype, out, keepdims,
               where=where, upcast_f16_for_computation=(dtype is None))

