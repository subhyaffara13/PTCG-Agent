
def histogram2d(
    x,
    y,
    bins=10,
    range: ArrayLike | None = None,
    normed=None,
    weights: ArrayLike | None = None,
    density=None,
):
    # vendored from https://github.com/numpy/numpy/blob/v1.24.0/numpy/lib/twodim_base.py#L655-L821
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N != 1 and N != 2:
        bins = [bins, bins]

    h, e = histogramdd((x, y), bins, range, normed, weights, density)

    return h, e[0], e[1]


def histogram2d(x, y, bins=10, range=None, density=None, weights=None):
    """
    Compute the bi-dimensional histogram of two data samples.

    Parameters
    ----------
    x : array_like, shape (N,)
        An array containing the x coordinates of the points to be
        histogrammed.
    y : array_like, shape (N,)
        An array containing the y coordinates of the points to be
        histogrammed.
    bins : int or array_like or [int, int] or [array, array], optional
        The bin specification:

        * If int, the number of bins for the two dimensions (nx=ny=bins).
        * If array_like, the bin edges for the two dimensions
          (x_edges=y_edges=bins).
        * If [int, int], the number of bins in each dimension
          (nx, ny = bins).
        * If [array, array], the bin edges in each dimension
          (x_edges, y_edges = bins).
        * A combination [int, array] or [array, int], where int
          is the number of bins and array is the bin edges.

    range : array_like, shape(2,2), optional
        The leftmost and rightmost edges of the bins along each dimension
        (if not specified explicitly in the `bins` parameters):
        ``[[xmin, xmax], [ymin, ymax]]``. All values outside of this range
        will be considered outliers and not tallied in the histogram.
    density : bool, optional
        If False, the default, returns the number of samples in each bin.
        If True, returns the probability *density* function at the bin,
        ``bin_count / sample_count / bin_area``.
    weights : array_like, shape(N,), optional
        An array of values ``w_i`` weighing each sample ``(x_i, y_i)``.
        Weights are normalized to 1 if `density` is True. If `density` is
        False, the values of the returned histogram are equal to the sum of
        the weights belonging to the samples falling into each bin.

    Returns
    -------
    H : ndarray, shape(nx, ny)
        The bi-dimensional histogram of samples `x` and `y`. Values in `x`
        are histogrammed along the first dimension and values in `y` are
        histogrammed along the second dimension.
    xedges : ndarray, shape(nx+1,)
        The bin edges along the first dimension.
    yedges : ndarray, shape(ny+1,)
        The bin edges along the second dimension.

    See Also
    --------
    histogram : 1D histogram
    histogramdd : Multidimensional histogram

    Notes
    -----
    When `density` is True, then the returned histogram is the sample
    density, defined such that the sum over bins of the product
    ``bin_value * bin_area`` is 1.

    Please note that the histogram does not follow the Cartesian convention
    where `x` values are on the abscissa and `y` values on the ordinate
    axis.  Rather, `x` is histogrammed along the first dimension of the
    array (vertical), and `y` along the second dimension of the array
    (horizontal).  This ensures compatibility with `histogramdd`.

    Examples
    --------
    >>> import numpy as np
    >>> from matplotlib.image import NonUniformImage
    >>> import matplotlib.pyplot as plt

    Construct a 2-D histogram with variable bin width. First define the bin
    edges:

    >>> xedges = [0, 1, 3, 5]
    >>> yedges = [0, 2, 3, 4, 6]

    Next we create a histogram H with random bin content:

    >>> x = np.random.normal(2, 1, 100)
    >>> y = np.random.normal(1, 1, 100)
    >>> H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    >>> # Histogram does not follow Cartesian convention (see Notes),
    >>> # therefore transpose H for visualization purposes.
    >>> H = H.T

    :func:`imshow <matplotlib.pyplot.imshow>` can only display square bins:

    >>> fig = plt.figure(figsize=(7, 3))
    >>> ax = fig.add_subplot(131, title='imshow: square bins')
    >>> plt.imshow(H, interpolation='nearest', origin='lower',
    ...         extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    <matplotlib.image.AxesImage object at 0x...>

    :func:`pcolormesh <matplotlib.pyplot.pcolormesh>` can display actual edges:

    >>> ax = fig.add_subplot(132, title='pcolormesh: actual edges',
    ...         aspect='equal')
    >>> X, Y = np.meshgrid(xedges, yedges)
    >>> ax.pcolormesh(X, Y, H)
    <matplotlib.collections.QuadMesh object at 0x...>

    :class:`NonUniformImage <matplotlib.image.NonUniformImage>` can be used to
    display actual bin edges with interpolation:

    >>> ax = fig.add_subplot(133, title='NonUniformImage: interpolated',
    ...         aspect='equal', xlim=xedges[[0, -1]], ylim=yedges[[0, -1]])
    >>> im = NonUniformImage(ax, interpolation='bilinear')
    >>> xcenters = (xedges[:-1] + xedges[1:]) / 2
    >>> ycenters = (yedges[:-1] + yedges[1:]) / 2
    >>> im.set_data(xcenters, ycenters, H)
    >>> ax.add_image(im)
    >>> plt.show()

    It is also possible to construct a 2-D histogram without specifying bin
    edges:

    >>> # Generate non-symmetric test data
    >>> n = 10000
    >>> x = np.linspace(1, 100, n)
    >>> y = 2*np.log(x) + np.random.rand(n) - 0.5
    >>> # Compute 2d histogram. Note the order of x/y and xedges/yedges
    >>> H, yedges, xedges = np.histogram2d(y, x, bins=20)

    Now we can plot the histogram using
    :func:`pcolormesh <matplotlib.pyplot.pcolormesh>`, and a
    :func:`hexbin <matplotlib.pyplot.hexbin>` for comparison.

    >>> # Plot histogram using pcolormesh
    >>> fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
    >>> ax1.pcolormesh(xedges, yedges, H, cmap='rainbow')
    >>> ax1.plot(x, 2*np.log(x), 'k-')
    >>> ax1.set_xlim(x.min(), x.max())
    >>> ax1.set_ylim(y.min(), y.max())
    >>> ax1.set_xlabel('x')
    >>> ax1.set_ylabel('y')
    >>> ax1.set_title('histogram2d')
    >>> ax1.grid()

    >>> # Create hexbin plot for comparison
    >>> ax2.hexbin(x, y, gridsize=20, cmap='rainbow')
    >>> ax2.plot(x, 2*np.log(x), 'k-')
    >>> ax2.set_title('hexbin')
    >>> ax2.set_xlim(x.min(), x.max())
    >>> ax2.set_xlabel('x')
    >>> ax2.grid()

    >>> plt.show()
    """
    from numpy import histogramdd

    if len(x) != len(y):
        raise ValueError('x and y must have the same length.')

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N not in {1, 2}:
        xedges = yedges = asarray(bins)
        bins = [xedges, yedges]
    hist, edges = histogramdd([x, y], bins, range, density, weights)
    return hist, edges[0], edges[1]


def histogram2d(x: ArrayLike, y: ArrayLike, bins: ArrayLike | list[ArrayLike] = 10,
                range: Sequence[None | Array | Sequence[ArrayLike]] | None = None,
                weights: ArrayLike | None = None,
                density: bool | None = None) -> tuple[Array, Array, Array]:
  """Compute a 2-dimensional histogram.

  JAX implementation of :func:`numpy.histogram2d`.

  Args:
    x: one-dimensional array of x-values for points to be binned.
    y: one-dimensional array of y-values for points to be binned.
    bins: Specify the number of bins in the histogram (default: 10). ``bins``
      may also be an array specifying the locations of the bin edges, or a pair
      of integers or pair of arrays specifying the number of bins in each
      dimension.
    range: Pair of arrays or lists of the form ``[[xmin, xmax], [ymin, ymax]]``
      specifying the range of the data in each dimension. If not specified, the
      range is inferred from the data.
    weights: An optional array specifying the weights of the data points.
      Should be the same shape as ``x`` and ``y``. If not specified, each
      data point is weighted equally.
    density: If True, return the normalized histogram in units of counts
      per unit area. If False (default) return the (weighted) counts per bin.

  Returns:
    A tuple of arrays ``(histogram, x_edges, y_edges)``, where ``histogram``
    contains the aggregated data, and ``x_edges`` and ``y_edges`` specify the
    boundaries of the bins.

  See Also:
    - :func:`jax.numpy.histogram`: Compute the histogram of a 1D array.
    - :func:`jax.numpy.histogramdd`: Compute the histogram of an N-dimensional array.
    - :func:`jax.numpy.histogram_bin_edges`: Compute the bin edges for a histogram.

  Examples:
    >>> x = jnp.array([1, 2, 3, 10, 11, 15, 19, 25])
    >>> y = jnp.array([2, 5, 6, 8, 13, 16, 17, 18])
    >>> counts, x_edges, y_edges = jnp.histogram2d(x, y, bins=8)
    >>> counts.shape
    (8, 8)
    >>> x_edges
    Array([ 1.,  4.,  7., 10., 13., 16., 19., 22., 25.], dtype=float32)
    >>> y_edges
    Array([ 2.,  4.,  6.,  8., 10., 12., 14., 16., 18.], dtype=float32)

    Specifying the bin range:

    >>> counts, x_edges, y_edges = jnp.histogram2d(x, y, range=[(0, 25), (0, 25)], bins=5)
    >>> counts.shape
    (5, 5)
    >>> x_edges
    Array([ 0.,  5., 10., 15., 20., 25.], dtype=float32)
    >>> y_edges
    Array([ 0.,  5., 10., 15., 20., 25.], dtype=float32)

    Specifying the bin edges explicitly:

    >>> x_edges = jnp.array([0, 10, 20, 30])
    >>> y_edges = jnp.array([0, 10, 20, 30])
    >>> counts, _, _ = jnp.histogram2d(x, y, bins=[x_edges, y_edges])
    >>> counts
    Array([[3, 0, 0],
           [1, 3, 0],
           [0, 1, 0]], dtype=int32)

    Using ``density=True`` returns a normalized histogram:

    >>> density, x_edges, y_edges = jnp.histogram2d(x, y, density=True)
    >>> dx = jnp.diff(x_edges)
    >>> dy = jnp.diff(y_edges)
    >>> normed_sum = jnp.sum(density * dx[:, None] * dy[None, :])
    >>> jnp.allclose(normed_sum, 1.0)
    Array(True, dtype=bool)
  """
  x, y = util.ensure_arraylike("histogram2d", x, y)
  try:
    N = len(bins)  # pyrefly: ignore[bad-argument-type]
  except TypeError:
    N = 1

  if N != 1 and N != 2:
    x_edges = y_edges = asarray(bins)
    bins = [x_edges, y_edges]  # pyrefly: ignore[bad-assignment]

  sample = transpose(asarray([x, y]))
  hist, edges = histogramdd(sample, bins, range, weights, density)
  return hist, edges[0], edges[1]

