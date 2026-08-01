
def violin_stats(X, method=("GaussianKDE", "scott"), points=100, quantiles=None):
    """
    Return a list of dictionaries of data which can be used to draw a series
    of violin plots.

    See the ``Returns`` section below to view the required keys of the
    dictionary.

    Users can skip this function and pass a user-defined set of dictionaries
    with the same keys to `~.axes.Axes.violin` instead of using Matplotlib
    to do the calculations. See the *Returns* section below for the keys
    that must be present in the dictionaries.

    Parameters
    ----------
    X : 1D array or sequence of 1D arrays or 2D array
        Sample data that will be used to produce the gaussian kernel density
        estimates. Non-finite and masked values are ignored.
        Possible values:

        - 1D array: Statistics are computed for that array.
        - sequence of 1D arrays: Statistics are computed for each array in the sequence.
        - 2D array: Statistics are computed for each column in the array.

    method : (name, bw_method) or callable,
        The method used to calculate the kernel density estimate for each
        column of data. Valid values:

        - a tuple of the form ``(name, bw_method)`` where *name* currently must
          always be ``"GaussianKDE"`` and *bw_method* is the method used to
          calculate the estimator bandwidth. Supported values are 'scott',
          'silverman' or a float or a callable. If a float, this will be used
          directly as `!kde.factor`.  If a callable, it should take a
          `matplotlib.mlab.GaussianKDE` instance as its only parameter and
          return a float.

        - a callable with the signature ::

             def method(data: ndarray, coords: ndarray) -> ndarray

          It should return the KDE of *data* evaluated at *coords*.

          .. versionadded:: 3.11
             Support for ``(name, bw_method)`` tuple.

    points : int, default: 100
        Defines the number of points to evaluate each of the gaussian kernel
        density estimates at.

    quantiles : array-like, default: None
        Defines (if not None) a list of floats in interval [0, 1] for each
        column of data, which represents the quantiles that will be rendered
        for that column of data. Must have 2 or fewer dimensions. 1D array will
        be treated as a singleton list containing them.

    Returns
    -------
    list of dict
        A list of dictionaries containing the results for each column of data.
        The dictionaries contain at least the following:

        - coords: A list of scalars containing the coordinates this particular
          kernel density estimate was evaluated at.
        - vals: A list of scalars containing the values of the kernel density
          estimate at each of the coordinates given in *coords*.
        - mean: The mean value for this column of data.
        - median: The median value for this column of data.
        - min: The minimum value for this column of data.
        - max: The maximum value for this column of data.
        - quantiles: The quantile values for this column of data.
    """
    if isinstance(method, tuple):
        name, bw_method = method
        if name != "GaussianKDE":
            raise ValueError(f"Unknown KDE method name {name!r}. The only supported "
                             'named method is "GaussianKDE"')

        def _kde_method(x, coords):
            # fallback gracefully if the vector contains only one value
            if np.all(x[0] == x):
                return (x[0] == coords).astype(float)
            kde = mlab.GaussianKDE(x, bw_method)
            return kde.evaluate(coords)

        method = _kde_method

    # List of dictionaries describing each of the violins.
    vpstats = []

    # Want X to be a list of data sequences
    X = _reshape_2D(X, "X")

    # Want quantiles to be as the same shape as data sequences
    if quantiles is not None and len(quantiles) != 0:
        quantiles = _reshape_2D(quantiles, "quantiles")
    # Else, mock quantiles if it's none or empty
    else:
        quantiles = [[]] * len(X)

    # quantiles should have the same size as dataset
    if len(X) != len(quantiles):
        raise ValueError("List of violinplot statistics and quantiles values"
                         " must have the same length")

    # Zip x and quantiles
    for (x, quantile) in zip(X, quantiles):
        x = np.asarray(x)
        x, = delete_masked_points(x)

        if len(x) == 0:
            vpstats.append({
                'vals': np.array([]),
                'coords': np.array([]),
                'mean': np.nan,
                'median': np.nan,
                'min': np.nan,
                'max': np.nan,
                'quantiles': np.array([]),
            })
        else:
            min_val = np.min(x)
            max_val = np.max(x)
            coords = np.linspace(min_val, max_val, points)

            vpstats.append({
                'vals': method(x, coords),
                'coords': coords,
                'mean': np.mean(x),
                'median': np.median(x),
                'min': min_val,
                'max': max_val,
                'quantiles': np.atleast_1d(np.percentile(x, 100 * quantile))
            })

    return vpstats

