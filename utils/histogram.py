from typing import Callable

def histogram(items: Iterable[TItem]) -> dict[TItem, int]:
    """Accepts a list of hashable items and returns a dictionary where the keys are items and the values are counts of each item in the list."""
    results = {}
    for item in items:
        if item not in results:
            results[item] = 1
        else:
            results[item] += 1
    return results


def histogram(
    a: ArrayLike,
    bins: ArrayLike = 10,
    range=None,
    normed=None,
    weights: ArrayLike | None = None,
    density=None,
):
    if normed is not None:
        raise ValueError("normed argument is deprecated, use density= instead")

    if weights is not None and weights.dtype.is_complex:
        raise NotImplementedError("complex weights histogram.")

    is_a_int = not (a.dtype.is_floating_point or a.dtype.is_complex)
    is_w_int = weights is None or not weights.dtype.is_floating_point
    if is_a_int:
        a = a.double()

    if weights is not None:
        weights = _util.cast_if_needed(weights, a.dtype)

    if isinstance(bins, torch.Tensor):
        if bins.ndim == 0:
            # bins was a single int
            bins = operator.index(bins)
        else:
            bins = _util.cast_if_needed(bins, a.dtype)

    if range is None:
        h, b = torch.histogram(a, bins, weight=weights, density=bool(density))
    else:
        h, b = torch.histogram(
            a, bins, range=range, weight=weights, density=bool(density)
        )

    if not density and is_w_int:
        h = h.long()
    if is_a_int:
        b = b.long()

    return h, b


def histogram(name, values, bins, max_bins=None):
    # pylint: disable=line-too-long
    """Output a `Summary` protocol buffer with a histogram.

    The generated
    [`Summary`](https://www.tensorflow.org/code/tensorflow/core/framework/summary.proto)
    has one summary value containing a histogram for `values`.
    This op reports an `InvalidArgument` error if any value is not finite.
    Args:
      name: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      values: A real numeric `Tensor`. Any shape. Values to use to
        build the histogram.
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    values = make_np(values)
    hist = make_histogram(values.astype(float), bins, max_bins)
    return Summary(value=[Summary.Value(tag=name, histo=hist)])


def histogram(input, min, max, bins, labels=None, index=None):
    """
    Calculate the histogram of the values of an array, optionally at labels.

    Histogram calculates the frequency of values in an array within bins
    determined by `min`, `max`, and `bins`. The `labels` and `index`
    keywords can limit the scope of the histogram to specified sub-regions
    within the array.

    Parameters
    ----------
    input : array_like
        Data for which to calculate histogram.
    min, max : int
        Minimum and maximum values of range of histogram bins.
    bins : int
        Number of bins.
    labels : array_like, optional
        Labels for objects in `input`.
        If not None, must be same shape as `input`.
    index : int or sequence of ints, optional
        Label or labels for which to calculate histogram. If None, all values
        where label is greater than zero are used

    Returns
    -------
    hist : ndarray
        Histogram counts.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[ 0.    ,  0.2146,  0.5962,  0.    ],
    ...               [ 0.    ,  0.7778,  0.    ,  0.    ],
    ...               [ 0.    ,  0.    ,  0.    ,  0.    ],
    ...               [ 0.    ,  0.    ,  0.7181,  0.2787],
    ...               [ 0.    ,  0.    ,  0.6573,  0.3094]])
    >>> from scipy import ndimage
    >>> ndimage.histogram(a, 0, 1, 10)
    array([13,  0,  2,  1,  0,  1,  1,  2,  0,  0])

    With labels and no indices, non-zero elements are counted:

    >>> lbl, nlbl = ndimage.label(a)
    >>> ndimage.histogram(a, 0, 1, 10, lbl)
    array([0, 0, 2, 1, 0, 1, 1, 2, 0, 0])

    Indices can be used to count only certain objects:

    >>> ndimage.histogram(a, 0, 1, 10, lbl, 2)
    array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0])

    """
    _bins = np.linspace(min, max, bins + 1)

    def _hist(vals):
        return np.histogram(vals, _bins)[0]

    return labeled_comprehension(input, labels, index, _hist, object, None,
                                 pass_positions=False)


def histogram(a, bins=10, range=None, density=None, weights=None):
    r"""
    Compute the histogram of a dataset.

    Parameters
    ----------
    a : array_like
        Input data. The histogram is computed over the flattened array.
    bins : int or sequence of scalars or str, optional
        If `bins` is an int, it defines the number of equal-width
        bins in the given range (10, by default). If `bins` is a
        sequence, it defines a monotonically increasing array of bin edges,
        including the rightmost edge, allowing for non-uniform bin widths.

        If `bins` is a string, it defines the method used to calculate the
        optimal bin width, as defined by `histogram_bin_edges`.

    range : (float, float), optional
        The lower and upper range of the bins.  If not provided, range
        is simply ``(a.min(), a.max())``.  Values outside the range are
        ignored. The first element of the range must be less than or
        equal to the second. `range` affects the automatic bin
        computation as well. While bin width is computed to be optimal
        based on the actual data within `range`, the bin count will fill
        the entire range including portions containing no data.
    weights : array_like, optional
        An array of weights, of the same shape as `a`.  Each value in
        `a` only contributes its associated weight towards the bin count
        (instead of 1). If `density` is True, the weights are
        normalized, so that the integral of the density over the range
        remains 1.
        Please note that the ``dtype`` of `weights` will also become the
        ``dtype`` of the returned accumulator (`hist`), so it must be
        large enough to hold accumulated values as well.
    density : bool, optional
        If ``False``, the result will contain the number of samples in
        each bin. If ``True``, the result is the value of the
        probability *density* function at the bin, normalized such that
        the *integral* over the range is 1. Note that the sum of the
        histogram values will not be equal to 1 unless bins of unity
        width are chosen; it is not a probability *mass* function.

    Returns
    -------
    hist : array
        The values of the histogram. See `density` and `weights` for a
        description of the possible semantics.  If `weights` are given,
        ``hist.dtype`` will be taken from `weights`.
    bin_edges : array of dtype float
        Return the bin edges ``(length(hist)+1)``.


    See Also
    --------
    histogramdd, bincount, searchsorted, digitize, histogram_bin_edges

    Notes
    -----
    All but the last (righthand-most) bin is half-open.  In other words,
    if `bins` is::

      [1, 2, 3, 4]

    then the first bin is ``[1, 2)`` (including 1, but excluding 2) and
    the second ``[2, 3)``.  The last bin, however, is ``[3, 4]``, which
    *includes* 4.


    Examples
    --------
    >>> import numpy as np
    >>> np.histogram([1, 2, 1], bins=[0, 1, 2, 3])
    (array([0, 2, 1]), array([0, 1, 2, 3]))
    >>> np.histogram(np.arange(4), bins=np.arange(5), density=True)
    (array([0.25, 0.25, 0.25, 0.25]), array([0, 1, 2, 3, 4]))
    >>> np.histogram([[1, 2, 1], [1, 0, 1]], bins=[0,1,2,3])
    (array([1, 4, 1]), array([0, 1, 2, 3]))

    >>> a = np.arange(5)
    >>> hist, bin_edges = np.histogram(a, density=True)
    >>> hist
    array([0.5, 0. , 0.5, 0. , 0. , 0.5, 0. , 0.5, 0. , 0.5])
    >>> hist.sum()
    2.4999999999999996
    >>> np.sum(hist * np.diff(bin_edges))
    1.0

    Automated Bin Selection Methods example, using 2 peak random data
    with 2000 points.

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        import numpy as np

        rng = np.random.RandomState(10)  # deterministic random data
        a = np.hstack((rng.normal(size=1000),
                       rng.normal(loc=5, scale=2, size=1000)))
        plt.hist(a, bins='auto')  # arguments are passed to np.histogram
        plt.title("Histogram with 'auto' bins")
        plt.show()

    """
    a, weights = _ravel_and_check_weights(a, weights)

    bin_edges, uniform_bins = _get_bin_edges(a, bins, range, weights)

    # Histogram is an integer or a float array depending on the weights.
    if weights is None:
        ntype = np.dtype(np.intp)
    else:
        ntype = weights.dtype

    # We set a block size, as this allows us to iterate over chunks when
    # computing histograms, to minimize memory usage.
    BLOCK = 65536

    # The fast path uses bincount, but that only works for certain types
    # of weight
    simple_weights = (
        weights is None or
        np.can_cast(weights.dtype, np.double) or
        np.can_cast(weights.dtype, complex)
    )

    if uniform_bins is not None and simple_weights:
        # Fast algorithm for equal bins
        # We now convert values of a to bin indices, under the assumption of
        # equal bin widths (which is valid here).
        first_edge, last_edge, n_equal_bins = uniform_bins

        # Initialize empty histogram
        n = np.zeros(n_equal_bins, ntype)

        # Pre-compute histogram scaling factor
        norm_numerator = n_equal_bins
        norm_denom = _unsigned_subtract(last_edge, first_edge)

        # We iterate over blocks here for two reasons: the first is that for
        # large arrays, it is actually faster (for example for a 10^8 array it
        # is 2x as fast) and it results in a memory footprint 3x lower in the
        # limit of large arrays.
        for i in _range(0, len(a), BLOCK):
            tmp_a = a[i:i + BLOCK]
            if weights is None:
                tmp_w = None
            else:
                tmp_w = weights[i:i + BLOCK]

            # Only include values in the right range
            keep = (tmp_a >= first_edge)
            keep &= (tmp_a <= last_edge)
            if not np.logical_and.reduce(keep):
                tmp_a = tmp_a[keep]
                if tmp_w is not None:
                    tmp_w = tmp_w[keep]

            # This cast ensures no type promotions occur below, which gh-10322
            # make unpredictable. Getting it wrong leads to precision errors
            # like gh-8123.
            tmp_a = tmp_a.astype(bin_edges.dtype, copy=False)

            # Compute the bin indices, and for values that lie exactly on
            # last_edge we need to subtract one
            f_indices = ((_unsigned_subtract(tmp_a, first_edge) / norm_denom)
                         * norm_numerator)
            indices = f_indices.astype(np.intp)
            indices[indices == n_equal_bins] -= 1

            # The index computation is not guaranteed to give exactly
            # consistent results within ~1 ULP of the bin edges.
            decrement = tmp_a < bin_edges[indices]
            indices[decrement] -= 1
            # The last bin includes the right edge. The other bins do not.
            increment = ((tmp_a >= bin_edges[indices + 1])
                         & (indices != n_equal_bins - 1))
            indices[increment] += 1

            # We now compute the histogram using bincount
            if ntype.kind == 'c':
                n.real += np.bincount(indices, weights=tmp_w.real,
                                      minlength=n_equal_bins)
                n.imag += np.bincount(indices, weights=tmp_w.imag,
                                      minlength=n_equal_bins)
            else:
                n += np.bincount(indices, weights=tmp_w,
                                 minlength=n_equal_bins).astype(ntype)
    else:
        # Compute via cumulative histogram
        cum_n = np.zeros(bin_edges.shape, ntype)
        if weights is None:
            for i in _range(0, len(a), BLOCK):
                sa = np.sort(a[i:i + BLOCK])
                cum_n += _search_sorted_inclusive(sa, bin_edges)
        else:
            zero = np.zeros(1, dtype=ntype)
            for i in _range(0, len(a), BLOCK):
                tmp_a = a[i:i + BLOCK]
                tmp_w = weights[i:i + BLOCK]
                sorting_index = np.argsort(tmp_a)
                sa = tmp_a[sorting_index]
                sw = tmp_w[sorting_index]
                cw = np.concatenate((zero, sw.cumsum()))
                bin_index = _search_sorted_inclusive(sa, bin_edges)
                cum_n += cw[bin_index]

        n = np.diff(cum_n)

    if density:
        db = np.array(np.diff(bin_edges), float)
        return n / db / n.sum(), bin_edges

    return n, bin_edges


def histogram(result: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.RankedTensorType], *, mask: _Optional[_ods_ir.Value] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return HistogramOp(result=result, src=src, mask=mask, loc=loc, ip=ip).result


def histogram(jaxpr: core.Jaxpr, key: Callable,
              key_fmt: Callable = lambda x: x):
  d = collect_eqns(jaxpr, key)
  return {key_fmt(k): len(v) for k, v in d.items()}


def histogram(a: ArrayLike, bins: ArrayLike = 10,
              range: Sequence[ArrayLike] | None = None,
              weights: ArrayLike | None = None,
              density: bool | None = None) -> tuple[Array, Array]:
  """Compute a 1-dimensional histogram.

  JAX implementation of :func:`numpy.histogram`.

  Args:
    a: array of values to be binned. May be any size or dimension.
    bins: Specify the number of bins in the histogram (default: 10). ``bins``
      may also be an array specifying the locations of the bin edges.
    range: tuple of scalars. Specifies the range of the data. If not specified,
      the range is inferred from the data.
    weights: An optional array specifying the weights of the data points.
      Should be broadcast-compatible with ``a``. If not specified, each
      data point is weighted equally.
    density: If True, return the normalized histogram in units of counts
      per unit length. If False (default) return the (weighted) counts per bin.

  Returns:
    A tuple of arrays ``(histogram, bin_edges)``, where ``histogram`` contains
    the aggregated data, and ``bin_edges`` specifies the boundaries of the bins.

  See Also:
    - :func:`jax.numpy.bincount`: Count the number of occurrences of each value in an array.
    - :func:`jax.numpy.histogram2d`: Compute the histogram of a 2D array.
    - :func:`jax.numpy.histogramdd`: Compute the histogram of an N-dimensional array.
    - :func:`jax.numpy.histogram_bin_edges`: Compute the bin edges for a histogram.

  Examples:
    >>> a = jnp.array([1, 2, 3, 10, 11, 15, 19, 25])
    >>> counts, bin_edges = jnp.histogram(a, bins=8)
    >>> print(counts)
    [3. 0. 0. 2. 1. 0. 1. 1.]
    >>> print(bin_edges)
    [ 1.  4.  7. 10. 13. 16. 19. 22. 25.]

    Specifying the bin range:

    >>> counts, bin_edges = jnp.histogram(a, range=(0, 25), bins=5)
    >>> print(counts)
    [3. 0. 2. 2. 1.]
    >>> print(bin_edges)
    [ 0.  5. 10. 15. 20. 25.]

    Specifying the bin edges explicitly:

    >>> bin_edges = jnp.array([0, 10, 20, 30])
    >>> counts, _ = jnp.histogram(a, bins=bin_edges)
    >>> print(counts)
    [3. 4. 1.]

    Using ``density=True`` returns a normalized histogram:

    >>> density, bin_edges = jnp.histogram(a, density=True)
    >>> dx = jnp.diff(bin_edges)
    >>> normed_sum = jnp.sum(density * dx)
    >>> jnp.allclose(normed_sum, 1.0)
    Array(True, dtype=bool)
  """
  if weights is None:
    a, _ = util.ensure_arraylike("histogram", a, bins)
    a, = util.promote_dtypes_inexact(a)
    weights = array_creation.ones_like(a)
  else:
    a, _, weights = util.ensure_arraylike("histogram", a, bins, weights)
    if np.shape(a) != np.shape(weights):
      raise ValueError("weights should have the same shape as a.")
    a, weights = util.promote_dtypes_inexact(a, weights)

  bin_edges = histogram_bin_edges(a, bins, range, weights)
  bin_idx = searchsorted(bin_edges, a, side='right')
  bin_idx = where(a == bin_edges[-1], len(bin_edges) - 1, bin_idx)
  counts = array_creation.zeros(len(bin_edges), weights.dtype).at[bin_idx].add(weights)[1:]
  if density:
    bin_widths = diff(bin_edges)
    counts = counts / bin_widths / counts.sum()
  return counts, bin_edges

