
def median(
    input: Tensor | MaskedTensor,
    dim: int = -1,
    *,
    keepdim: bool = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
By definition, the identity value of a median operation is the median
value of the tensor. If all elements of the input tensor along given
dimension(s) :attr:`dim` are masked-out, the identity value of the
median is undefined.  Due to this ambiguity, the elements of output
tensor with strided layout, that correspond to fully masked-out
elements, have ``nan`` values.
{reduction_args}
{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    is_float = torch.is_floating_point(input)
    if not is_float:
        input = input.to(dtype=torch.float)
    mask_input = _combine_input_and_mask(median, input, mask)
    if mask_input.layout == torch.strided:
        output = torch.nanmedian(mask_input, dim_, keepdim).values
        if is_float:
            return output
        elif not is_float and not torch.isnan(output).any():
            return output.to(dtype=dtype)
        else:
            raise ValueError(
                "masked median expects no fully masked out rows if dtype is not floating point"
            )
    else:
        raise ValueError(
            f"masked median expects strided tensor (got {mask_input.layout} tensor)"
        )


def median(
    a: ArrayLike,
    axis=None,
    out: OutArray | None = None,
    overwrite_input=False,
    keepdims: KeepDims = False,
):
    return quantile(
        a,
        torch.as_tensor(0.5),
        axis=axis,
        overwrite_input=overwrite_input,
        out=out,
        keepdims=keepdims,
    )


def median(X, evaluate=True, **kwargs):
    r"""
    Calculates the median of the probability distribution.

    Explanation
    ===========

    Mathematically, median of Probability distribution is defined as all those
    values of `m` for which the following condition is satisfied

    .. math::
        P(X\leq m) \geq  \frac{1}{2} \text{ and} \text{ } P(X\geq m)\geq \frac{1}{2}

    Parameters
    ==========

    X: The random expression whose median is to be calculated.

    Returns
    =======

    The FiniteSet or an Interval which contains the median of the
    random expression.

    Examples
    ========

    >>> from sympy.stats import Normal, Die, median
    >>> N = Normal('N', 3, 1)
    >>> median(N)
    {3}
    >>> D = Die('D')
    >>> median(D)
    {3, 4}

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Median#Probability_distributions

    """
    if not is_random(X):
        return X

    from sympy.stats.crv import ContinuousPSpace
    from sympy.stats.drv import DiscretePSpace
    from sympy.stats.frv import FinitePSpace

    if isinstance(pspace(X), FinitePSpace):
        cdf = pspace(X).compute_cdf(X)
        result = []
        for key, value in cdf.items():
            if value>= Rational(1, 2) and (1 - value) + \
            pspace(X).probability(Eq(X, key)) >= Rational(1, 2):
                result.append(key)
        return FiniteSet(*result)
    if isinstance(pspace(X), (ContinuousPSpace, DiscretePSpace)):
        cdf = pspace(X).compute_cdf(X)
        x = Dummy('x')
        result = solveset(piecewise_fold(cdf(x) - Rational(1, 2)), x, pspace(X).set)
        return result
    raise NotImplementedError("The median of %s is not implemented."%str(pspace(X)))


def median(input, labels=None, index=None):
    """
    Calculate the median of the values of an array over labeled regions.

    Parameters
    ----------
    input : array_like
        Array_like of values. For each region specified by `labels`, the
        median value of `input` over the region is computed.
    labels : array_like, optional
        An array_like of integers marking different regions over which the
        median value of `input` is to be computed. `labels` must have the
        same shape as `input`. If `labels` is not specified, the median
        over the whole array is returned.
    index : array_like, optional
        A list of region labels that are taken into account for computing the
        medians. If index is None, the median over all elements where `labels`
        is non-zero is returned.

    Returns
    -------
    median : float or list of floats
        List of medians of `input` over the regions determined by `labels` and
        whose index is in `index`. If `index` or `labels` are not specified, a
        float is returned: the median value of `input` if `labels` is None,
        and the median value of elements where `labels` is greater than zero
        if `index` is None.

    See Also
    --------
    label, minimum, maximum, extrema, sum, mean, variance, standard_deviation

    Notes
    -----
    The function returns a Python list and not a NumPy array, use
    `np.array` to convert the list to an array.

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 1],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> labels, labels_nb = ndimage.label(a)
    >>> labels
    array([[1, 1, 0, 2],
           [1, 1, 0, 2],
           [0, 0, 0, 2],
           [3, 3, 0, 0]], dtype=int32)
    >>> ndimage.median(a, labels=labels, index=np.arange(1, labels_nb + 1))
    [2.5, 4.0, 6.0]
    >>> ndimage.median(a)
    1.0
    >>> ndimage.median(a, labels=labels)
    3.0

    """
    return _select(input, labels, index, find_median=True)[0]


def median(y):
    """
    Perform median/WPGMC linkage.

    See `linkage` for more information on the return structure
    and algorithm.

    The following are common calling conventions:

    1. ``Z = median(y)``:
       Performs median/WPGMC linkage on the condensed distance matrix
       ``y``.  See ``linkage`` for more information on the return
       structure and algorithm.
    2. ``Z = median(X)``:
       Performs median/WPGMC linkage on the observation matrix ``X``
       using Euclidean distance as the distance metric. See `linkage`
       for more information on the return structure and algorithm.

    Parameters
    ----------
    y : ndarray
        A condensed distance matrix. A condensed
        distance matrix is a flat array containing the upper
        triangular of the distance matrix. This is the form that
        ``pdist`` returns.  Alternatively, a collection of
        m observation vectors in n dimensions may be passed as
        an m by n array.

    Returns
    -------
    Z : ndarray
        The hierarchical clustering encoded as a linkage matrix.

    See Also
    --------
    linkage : for advanced creation of hierarchical clusterings.
    scipy.spatial.distance.pdist : pairwise distance metrics

    Examples
    --------
    >>> from scipy.cluster.hierarchy import median, fcluster
    >>> from scipy.spatial.distance import pdist

    First, we need a toy dataset to play with::

        x x    x x
        x        x

        x        x
        x x    x x

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    Then, we get a condensed distance matrix from this dataset:

    >>> y = pdist(X)

    Finally, we can perform the clustering:

    >>> Z = median(y)
    >>> Z
    array([[ 0.        ,  1.        ,  1.        ,  2.        ],
           [ 3.        ,  4.        ,  1.        ,  2.        ],
           [ 9.        , 10.        ,  1.        ,  2.        ],
           [ 6.        ,  7.        ,  1.        ,  2.        ],
           [ 2.        , 12.        ,  1.11803399,  3.        ],
           [ 5.        , 13.        ,  1.11803399,  3.        ],
           [ 8.        , 15.        ,  1.11803399,  3.        ],
           [11.        , 14.        ,  1.11803399,  3.        ],
           [18.        , 19.        ,  3.        ,  6.        ],
           [16.        , 17.        ,  3.5       ,  6.        ],
           [20.        , 21.        ,  3.25      , 12.        ]])

    The linkage matrix ``Z`` represents a dendrogram - see
    `scipy.cluster.hierarchy.linkage` for a detailed explanation of its
    contents.

    We can use `scipy.cluster.hierarchy.fcluster` to see to which cluster
    each initial point would belong given a distance threshold:

    >>> fcluster(Z, 0.9, criterion='distance')
    array([ 7,  8,  9, 10, 11, 12,  1,  2,  3,  4,  5,  6], dtype=int32)
    >>> fcluster(Z, 1.1, criterion='distance')
    array([5, 5, 6, 7, 7, 8, 1, 1, 2, 3, 3, 4], dtype=int32)
    >>> fcluster(Z, 2, criterion='distance')
    array([3, 3, 3, 4, 4, 4, 1, 1, 1, 2, 2, 2], dtype=int32)
    >>> fcluster(Z, 4, criterion='distance')
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int32)

    Also, `scipy.cluster.hierarchy.dendrogram` can be used to generate a
    plot of the dendrogram.

    """
    return linkage(y, method='median', metric='euclidean')


def median(a, axis=None, out=None, overwrite_input=False, keepdims=False):
    """
    Compute the median along the specified axis.

    Returns the median of the array elements.

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : {int, sequence of int, None}, optional
        Axis or axes along which the medians are computed. The default,
        axis=None, will compute the median along a flattened version of
        the array. If a sequence of axes, the array is first flattened
        along the given axes, then the median is computed along the
        resulting flattened axis.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output,
        but the type (of the output) will be cast if necessary.
    overwrite_input : bool, optional
       If True, then allow use of memory of input array `a` for
       calculations. The input array will be modified by the call to
       `median`. This will save memory when you do not need to preserve
       the contents of the input array. Treat the input as undefined,
       but it will probably be fully or partially sorted. Default is
       False. If `overwrite_input` is ``True`` and `a` is not already an
       `ndarray`, an error will be raised.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `arr`.

    Returns
    -------
    median : ndarray
        A new array holding the result. If the input contains integers
        or floats smaller than ``float64``, then the output data-type is
        ``np.float64``.  Otherwise, the data-type of the output is the
        same as that of the input. If `out` is specified, that array is
        returned instead.

    See Also
    --------
    mean, percentile

    Notes
    -----
    Given a vector ``V`` of length ``N``, the median of ``V`` is the
    middle value of a sorted copy of ``V``, ``V_sorted`` - i
    e., ``V_sorted[(N-1)/2]``, when ``N`` is odd, and the average of the
    two middle values of ``V_sorted`` when ``N`` is even.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[10, 7, 4], [3, 2, 1]])
    >>> a
    array([[10,  7,  4],
           [ 3,  2,  1]])
    >>> np.median(a)
    np.float64(3.5)
    >>> np.median(a, axis=0)
    array([6.5, 4.5, 2.5])
    >>> np.median(a, axis=1)
    array([7.,  2.])
    >>> np.median(a, axis=(0, 1))
    np.float64(3.5)
    >>> m = np.median(a, axis=0)
    >>> out = np.zeros_like(m)
    >>> np.median(a, axis=0, out=m)
    array([6.5,  4.5,  2.5])
    >>> m
    array([6.5,  4.5,  2.5])
    >>> b = a.copy()
    >>> np.median(b, axis=1, overwrite_input=True)
    array([7.,  2.])
    >>> assert not np.all(a==b)
    >>> b = a.copy()
    >>> np.median(b, axis=None, overwrite_input=True)
    np.float64(3.5)
    >>> assert not np.all(a==b)

    """
    return _ureduce(a, func=_median, keepdims=keepdims, axis=axis, out=out,
                    overwrite_input=overwrite_input)


def median(a, axis=None, out=None, overwrite_input=False, keepdims=False):
    """
    Compute the median along the specified axis.

    Returns the median of the array elements.

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : int, optional
        Axis along which the medians are computed. The default (None) is
        to compute the median along a flattened version of the array.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type will be cast if necessary.
    overwrite_input : bool, optional
        If True, then allow use of memory of input array (a) for
        calculations. The input array will be modified by the call to
        median. This will save memory when you do not need to preserve
        the contents of the input array. Treat the input as undefined,
        but it will probably be fully or partially sorted. Default is
        False. Note that, if `overwrite_input` is True, and the input
        is not already an `ndarray`, an error will be raised.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

    Returns
    -------
    median : ndarray
        A new array holding the result is returned unless out is
        specified, in which case a reference to out is returned.
        Return data-type is `float64` for integers and floats smaller than
        `float64`, or the input data-type, otherwise.

    See Also
    --------
    mean

    Notes
    -----
    Given a vector ``V`` with ``N`` non masked values, the median of ``V``
    is the middle value of a sorted copy of ``V`` (``Vs``) - i.e.
    ``Vs[(N-1)/2]``, when ``N`` is odd, or ``{Vs[N/2 - 1] + Vs[N/2]}/2``
    when ``N`` is even.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array(np.arange(8), mask=[0]*4 + [1]*4)
    >>> np.ma.median(x)
    1.5

    >>> x = np.ma.array(np.arange(10).reshape(2, 5), mask=[0]*6 + [1]*4)
    >>> np.ma.median(x)
    2.5
    >>> np.ma.median(x, axis=-1, overwrite_input=True)
    masked_array(data=[2.0, 5.0],
                 mask=[False, False],
           fill_value=1e+20)

    """
    if not hasattr(a, 'mask'):
        m = np.median(getdata(a, subok=True), axis=axis,
                      out=out, overwrite_input=overwrite_input,
                      keepdims=keepdims)
        if isinstance(m, np.ndarray) and 1 <= m.ndim:
            return masked_array(m, copy=False)
        else:
            return m

    return _ureduce(a, func=_median, keepdims=keepdims, axis=axis, out=out,
                    overwrite_input=overwrite_input)


def median(a: ArrayLike, axis: int | tuple[int, ...] | None = None,
           out: None = None, overwrite_input: bool = False,
           keepdims: bool = False) -> Array:
  r"""Return the median of array elements along a given axis.

  JAX implementation of :func:`numpy.median`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      median to be computed. If None, median is computed for the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.
    overwrite_input: Unused by JAX.

  Returns:
    An array of the median along the given axis.

  See also:
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.max`: Compute the maximum of array elements over given axis.
    - :func:`jax.numpy.min`: Compute the minimum of array elements over given axis.

  Examples:
    By default, the median is computed for the flattened array.

    >>> x = jnp.array([[2, 4, 7, 1],
    ...                [3, 5, 9, 2],
    ...                [6, 1, 8, 3]])
    >>> jnp.median(x)
    Array(3.5, dtype=float32)

    If ``axis=1``, the median is computed along axis 1.

    >>> jnp.median(x, axis=1)
    Array([3. , 4. , 4.5], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.median(x, axis=1, keepdims=True)
    Array([[3. ],
           [4. ],
           [4.5]], dtype=float32)
  """
  a = ensure_arraylike("median", a)
  return quantile(a, 0.5, axis=axis, out=out, overwrite_input=overwrite_input,
                  keepdims=keepdims, method='midpoint')

