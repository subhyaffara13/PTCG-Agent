
def histogramdd(
    sample,
    bins=10,
    range: ArrayLike | None = None,
    normed=None,
    weights: ArrayLike | None = None,
    density=None,
):
    # have to normalize manually because `sample` interpretation differs
    # for a list of lists and a 2D array
    if normed is not None:
        raise ValueError("normed argument is deprecated, use density= instead")

    from ._normalizations import normalize_array_like, normalize_seq_array_like

    if isinstance(sample, (list, tuple)):
        sample = normalize_array_like(sample).T
    else:
        sample = normalize_array_like(sample)

    sample = torch.atleast_2d(sample)

    if not (sample.dtype.is_floating_point or sample.dtype.is_complex):
        sample = sample.double()

    # bins is either an int, or a sequence of ints or a sequence of arrays
    bins_is_array = not (
        isinstance(bins, int) or builtins.all(isinstance(b, int) for b in bins)
    )
    if bins_is_array:
        bins = normalize_seq_array_like(bins)
        bins_dtypes = [b.dtype for b in bins]
        bins = [_util.cast_if_needed(b, sample.dtype) for b in bins]

    if range is not None:
        range = range.flatten().tolist()

    if weights is not None:
        # range=... is required : interleave min and max values per dimension
        mm = sample.aminmax(dim=0)
        range = torch.cat(mm).reshape(2, -1).T.flatten()
        range = tuple(range.tolist())
        weights = _util.cast_if_needed(weights, sample.dtype)
        w_kwd = {"weight": weights}
    else:
        w_kwd = {}

    h, b = torch.histogramdd(sample, bins, range, density=bool(density), **w_kwd)

    if bins_is_array:
        b = [_util.cast_if_needed(bb, dtyp) for bb, dtyp in zip(b, bins_dtypes)]

    return h, b


def histogramdd(sample, bins=10, range=None, density=None, weights=None):
    """
    Compute the multidimensional histogram of some data.

    Parameters
    ----------
    sample : (N, D) array, or (N, D) array_like
        The data to be histogrammed.

        Note the unusual interpretation of sample when an array_like:

        * When an array, each row is a coordinate in a D-dimensional space -
          such as ``histogramdd(np.array([p1, p2, p3]))``.
        * When an array_like, each element is the list of values for single
          coordinate - such as ``histogramdd((X, Y, Z))``.

        The first form should be preferred.

    bins : sequence or int, optional
        The bin specification:

        * A sequence of arrays describing the monotonically increasing bin
          edges along each dimension.
        * The number of bins for each dimension (nx, ny, ... =bins)
        * The number of bins for all dimensions (nx=ny=...=bins).

    range : sequence, optional
        A sequence of length D, each an optional (lower, upper) tuple giving
        the outer bin edges to be used if the edges are not given explicitly in
        `bins`.
        An entry of None in the sequence results in the minimum and maximum
        values being used for the corresponding dimension.
        The default, None, is equivalent to passing a tuple of D None values.
    density : bool, optional
        If False, the default, returns the number of samples in each bin.
        If True, returns the probability *density* function at the bin,
        ``bin_count / sample_count / bin_volume``.
    weights : (N,) array_like, optional
        An array of values `w_i` weighing each sample `(x_i, y_i, z_i, ...)`.
        Weights are normalized to 1 if density is True. If density is False,
        the values of the returned histogram are equal to the sum of the
        weights belonging to the samples falling into each bin.

    Returns
    -------
    H : ndarray
        The multidimensional histogram of sample x. See density and weights
        for the different possible semantics.
    edges : tuple of ndarrays
        A tuple of D arrays describing the bin edges for each dimension.

    See Also
    --------
    histogram: 1-D histogram
    histogram2d: 2-D histogram

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> r = rng.normal(size=(100,3))
    >>> H, edges = np.histogramdd(r, bins = (5, 8, 4))
    >>> H.shape, edges[0].size, edges[1].size, edges[2].size
    ((5, 8, 4), 6, 9, 5)

    """

    try:
        # Sample is an ND-array.
        N, D = sample.shape
    except (AttributeError, ValueError):
        # Sample is a sequence of 1D arrays.
        sample = np.atleast_2d(sample).T
        N, D = sample.shape

    nbin = np.empty(D, np.intp)
    edges = D * [None]
    dedges = D * [None]
    if weights is not None:
        weights = np.asarray(weights)

    try:
        M = len(bins)
        if M != D:
            raise ValueError(
                'The dimension of bins must be equal to the dimension of the '
                'sample x.')
    except TypeError:
        # bins is an integer
        bins = D * [bins]

    # normalize the range argument
    if range is None:
        range = (None,) * D
    elif len(range) != D:
        raise ValueError('range argument must have one entry per dimension')

    # Create edge arrays
    for i in _range(D):
        if np.ndim(bins[i]) == 0:
            if bins[i] < 1:
                raise ValueError(
                    f'`bins[{i}]` must be positive, when an integer')
            smin, smax = _get_outer_edges(sample[:, i], range[i])
            try:
                n = operator.index(bins[i])

            except TypeError as e:
                raise TypeError(
                    f"`bins[{i}]` must be an integer, when a scalar"
                ) from e

            edges[i] = np.linspace(smin, smax, n + 1)
        elif np.ndim(bins[i]) == 1:
            edges[i] = np.asarray(bins[i])
            if np.any(edges[i][:-1] > edges[i][1:]):
                raise ValueError(
                    f'`bins[{i}]` must be monotonically increasing, when an array')
        else:
            raise ValueError(
                f'`bins[{i}]` must be a scalar or 1d array')

        nbin[i] = len(edges[i]) + 1  # includes an outlier on each end
        dedges[i] = np.diff(edges[i])

    # Compute the bin number each sample falls into.
    Ncount = tuple(
        # avoid np.digitize to work around gh-11022
        np.searchsorted(edges[i], sample[:, i], side='right')
        for i in _range(D)
    )

    # Using digitize, values that fall on an edge are put in the right bin.
    # For the rightmost bin, we want values equal to the right edge to be
    # counted in the last bin, and not as an outlier.
    for i in _range(D):
        # Find which points are on the rightmost edge.
        on_edge = (sample[:, i] == edges[i][-1])
        # Shift these points one bin to the left.
        Ncount[i][on_edge] -= 1

    # Compute the sample indices in the flattened histogram matrix.
    # This raises an error if the array is too large.
    xy = np.ravel_multi_index(Ncount, nbin)

    # Compute the number of repetitions in xy and assign it to the
    # flattened histmat.
    hist = np.bincount(xy, weights, minlength=nbin.prod())

    # Shape into a proper matrix
    hist = hist.reshape(nbin)

    # This preserves the (bad) behavior observed in gh-7845, for now.
    hist = hist.astype(float, casting='safe')

    # Remove outliers (indices 0 and -1 for each dimension).
    core = D * (slice(1, -1),)
    hist = hist[core]

    if density:
        # calculate the probability density function
        s = hist.sum()
        for i in _range(D):
            shape = np.ones(D, int)
            shape[i] = nbin[i] - 2
            hist = hist / dedges[i].reshape(shape)
        hist /= s

    if (hist.shape != nbin - 2).any():
        raise RuntimeError(
            "Internal Shape Error")
    return hist, edges


def histogramdd(sample: ArrayLike, bins: ArrayLike | list[ArrayLike] = 10,
                range: Sequence[None | Array | Sequence[ArrayLike]] | None = None,
                weights: ArrayLike | None = None,
                density: bool | None = None) -> tuple[Array, list[Array]]:
  """Compute an N-dimensional histogram.

  JAX implementation of :func:`numpy.histogramdd`.

  Args:
    sample: input array of shape ``(N, D)`` representing ``N`` points in
      ``D`` dimensions.
    bins: Specify the number of bins in each dimension of the histogram.
      (default: 10). May also be a length-D sequence of integers or arrays
      of bin edges.
    range: Length-D sequence of pairs specifying the range for each dimension.
      If not specified, the range is inferred from the data.
    weights: An optional shape ``(N,)`` array specifying the weights of the
      data points.
      Should be the same shape as ``sample``. If not specified, each
      data point is weighted equally.
    density: If True, return the normalized histogram in units of counts
      per unit volume. If False (default) return the (weighted) counts per bin.

  Returns:
    A tuple of arrays ``(histogram, bin_edges)``, where ``histogram`` contains
    the aggregated data, and ``bin_edges`` specifies the boundaries of the bins.

  See Also:
    - :func:`jax.numpy.histogram`: Compute the histogram of a 1D array.
    - :func:`jax.numpy.histogram2d`: Compute the histogram of a 2D array.
    - :func:`jax.numpy.histogram_bin_edges`: Compute the bin edges for a histogram.

  Examples:
    A histogram over 100 points in three dimensions

    >>> key = jax.random.key(42)
    >>> a = jax.random.normal(key, (100, 3))
    >>> counts, bin_edges = jnp.histogramdd(a, bins=6,
    ...                                     range=[(-3, 3), (-3, 3), (-3, 3)])
    >>> counts.shape
    (6, 6, 6)
    >>> bin_edges  # doctest: +SKIP
    [Array([-3., -2., -1.,  0.,  1.,  2.,  3.], dtype=float32),
     Array([-3., -2., -1.,  0.,  1.,  2.,  3.], dtype=float32),
     Array([-3., -2., -1.,  0.,  1.,  2.,  3.], dtype=float32)]

    Using ``density=True`` returns a normalized histogram:

    >>> density, bin_edges = jnp.histogramdd(a, density=True)
    >>> bin_widths = map(jnp.diff, bin_edges)
    >>> dx, dy, dz = jnp.meshgrid(*bin_widths, indexing='ij')
    >>> normed = jnp.sum(density * dx * dy * dz)
    >>> jnp.allclose(normed, 1.0)
    Array(True, dtype=bool)
  """
  if weights is None:
    sample = util.ensure_arraylike("histogramdd", sample)
    sample, = util.promote_dtypes_inexact(sample)
  else:
    sample, weights = util.ensure_arraylike("histogramdd", sample, weights)
    if np.shape(weights) != np.shape(sample)[:1]:
      raise ValueError("should have one weight for each sample.")
    sample, weights = util.promote_dtypes_inexact(sample, weights)
  N, D = np.shape(sample)

  if range is not None and (
      len(range) != D or any(r is not None and np.shape(r)[0] != 2 for r in range)):  # pyrefly: ignore[no-matching-overload]
    raise ValueError(f"For sample.shape={(N, D)}, range must be a sequence "
                     f"of {D} pairs or Nones; got {range=}")

  try:
    bins_per_dimension = list(bins)  # pyrefly: ignore[bad-argument-type]
  except TypeError:
    # when bin_size is integer, the same bin is used for each dimension
    bins_per_dimension: list[ArrayLike] = D * [bins]  # pyrefly: ignore[bad-assignment]
  else:
    if len(bins_per_dimension) != D:
      raise ValueError("should be a bin for each dimension.")

  bin_idx_by_dim: list[Array] = []
  bin_edges_by_dim: list[Array] = []

  for i in builtins.range(D):
    range_i = None if range is None else range[i]
    bin_edges = histogram_bin_edges(sample[:, i], bins_per_dimension[i], range_i, weights)
    bin_idx = searchsorted(bin_edges, sample[:, i], side='right')
    bin_idx = where(sample[:, i] == bin_edges[-1], bin_idx - 1, bin_idx)
    bin_idx_by_dim.append(bin_idx)
    bin_edges_by_dim.append(bin_edges)

  nbins = tuple(len(bin_edges) + 1 for bin_edges in bin_edges_by_dim)
  dedges = [diff(bin_edges) for bin_edges in bin_edges_by_dim]

  xy = ravel_multi_index(tuple(bin_idx_by_dim), nbins, mode='clip')
  hist = bincount(xy, weights, length=math.prod(nbins))
  hist = reshape(hist, nbins)
  core = D*(slice(1, -1),)
  hist = hist[core]

  if density:
    hist = hist.astype(sample.dtype)
    hist /= hist.sum()
    for norm in ix_(*dedges):
      hist /= norm

  return hist, bin_edges_by_dim

