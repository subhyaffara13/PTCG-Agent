
def fit(
    image: Image.Image,
    size: tuple[int, int],
    method: int = Image.Resampling.BICUBIC,
    bleed: float = 0.0,
    centering: tuple[float, float] = (0.5, 0.5),
) -> Image.Image:
    """
    Returns a resized and cropped version of the image, cropped to the
    requested aspect ratio and size.

    This function was contributed by Kevin Cazabon.

    :param image: The image to resize and crop.
    :param size: The requested output size in pixels, given as a
                 (width, height) tuple.
    :param method: Resampling method to use. Default is
                   :py:attr:`~PIL.Image.Resampling.BICUBIC`.
                   See :ref:`concept-filters`.
    :param bleed: Remove a border around the outside of the image from all
                  four edges. The value is a decimal percentage (use 0.01 for
                  one percent). The default value is 0 (no border).
                  Cannot be greater than or equal to 0.5.
    :param centering: Control the cropping position.  Use (0.5, 0.5) for
                      center cropping (e.g. if cropping the width, take 50% off
                      of the left side, and therefore 50% off the right side).
                      (0.0, 0.0) will crop from the top left corner (i.e. if
                      cropping the width, take all of the crop off of the right
                      side, and if cropping the height, take all of it off the
                      bottom).  (1.0, 0.0) will crop from the bottom left
                      corner, etc. (i.e. if cropping the width, take all of the
                      crop off the left side, and if cropping the height take
                      none from the top, and therefore all off the bottom).
    :return: An image.
    """

    # by Kevin Cazabon, Feb 17/2000
    # kevin@cazabon.com
    # https://www.cazabon.com

    centering_x, centering_y = centering

    if not 0.0 <= centering_x <= 1.0:
        centering_x = 0.5
    if not 0.0 <= centering_y <= 1.0:
        centering_y = 0.5

    if not 0.0 <= bleed < 0.5:
        bleed = 0.0

    # calculate the area to use for resizing and cropping, subtracting
    # the 'bleed' around the edges

    # number of pixels to trim off on Top and Bottom, Left and Right
    bleed_pixels = (bleed * image.size[0], bleed * image.size[1])

    live_size = (
        image.size[0] - bleed_pixels[0] * 2,
        image.size[1] - bleed_pixels[1] * 2,
    )

    # calculate the aspect ratio of the live_size
    live_size_ratio = live_size[0] / live_size[1]

    # calculate the aspect ratio of the output image
    output_ratio = size[0] / size[1]

    # figure out if the sides or top/bottom will be cropped off
    if live_size_ratio == output_ratio:
        # live_size is already the needed ratio
        crop_width = live_size[0]
        crop_height = live_size[1]
    elif live_size_ratio >= output_ratio:
        # live_size is wider than what's needed, crop the sides
        crop_width = output_ratio * live_size[1]
        crop_height = live_size[1]
    else:
        # live_size is taller than what's needed, crop the top and bottom
        crop_width = live_size[0]
        crop_height = live_size[0] / output_ratio

    # make the crop
    crop_left = bleed_pixels[0] + (live_size[0] - crop_width) * centering_x
    crop_top = bleed_pixels[1] + (live_size[1] - crop_height) * centering_y

    crop = (crop_left, crop_top, crop_left + crop_width, crop_top + crop_height)

    # resize the image and return it
    return image.resize(size, method, box=crop)


def fit(dist, data, bounds=None, *, guess=None, method='mle',
        optimizer=optimize.differential_evolution):
    r"""Fit a discrete or continuous distribution to data.

    Given a distribution, data, and bounds on the parameters of the
    distribution, return maximum likelihood estimates of the parameters.

    Parameters
    ----------
    dist : `scipy.stats.rv_continuous` or `scipy.stats.rv_discrete`
        The object representing the distribution to be fit to the data.
    data : 1D array_like
        The data to which the distribution is to be fit. If the data contain
        any of ``np.nan``, ``np.inf``, or -``np.inf``, the fit method will
        raise a ``ValueError``.
    bounds : dict or sequence of tuples, optional
        If a dictionary, each key is the name of a parameter of the
        distribution, and the corresponding value is a tuple containing the
        lower and upper bound on that parameter.  If the distribution is
        defined only for a finite range of values of that parameter, no entry
        for that parameter is required; e.g., some distributions have
        parameters which must be on the interval [0, 1]. Bounds for parameters
        location (``loc``) and scale (``scale``) are optional; by default,
        they are fixed to 0 and 1, respectively.

        If a sequence, element *i* is a tuple containing the lower and upper
        bound on the *i*\ th parameter of the distribution. In this case,
        bounds for *all* distribution shape parameters must be provided.
        Optionally, bounds for location and scale may follow the
        distribution shape parameters.

        If a shape is to be held fixed (e.g. if it is known), the
        lower and upper bounds may be equal. If a user-provided lower or upper
        bound is beyond a bound of the domain for which the distribution is
        defined, the bound of the distribution's domain will replace the
        user-provided value. Similarly, parameters which must be integral
        will be constrained to integral values within the user-provided bounds.
    guess : dict or array_like, optional
        If a dictionary, each key is the name of a parameter of the
        distribution, and the corresponding value is a guess for the value
        of the parameter.

        If a sequence, element *i* is a guess for the *i*\ th parameter of the
        distribution. In this case, guesses for *all* distribution shape
        parameters must be provided.

        If `guess` is not provided, guesses for the decision variables will
        not be passed to the optimizer. If `guess` is provided, guesses for
        any missing parameters will be set at the mean of the lower and
        upper bounds. Guesses for parameters which must be integral will be
        rounded to integral values, and guesses that lie outside the
        intersection of the user-provided bounds and the domain of the
        distribution will be clipped.
    method : {'mle', 'mse'}
        With ``method="mle"`` (default), the fit is computed by minimizing
        the negative log-likelihood function. A large, finite penalty
        (rather than infinite negative log-likelihood) is applied for
        observations beyond the support of the distribution.
        With ``method="mse"``, the fit is computed by minimizing
        the negative log-product spacing function. The same penalty is applied
        for observations beyond the support. We follow the approach of [1]_,
        which is generalized for samples with repeated observations.
    optimizer : callable, optional
        `optimizer` is a callable that accepts the following positional
        argument.

        fun : callable
            The objective function to be optimized. `fun` accepts one argument
            ``x``, candidate shape parameters of the distribution, and returns
            the objective function value given ``x``, `dist`, and the provided
            `data`.
            The job of `optimizer` is to find values of the decision variables
            that minimizes `fun`.

        `optimizer` must also accept the following keyword argument.

        bounds : sequence of tuples
            The bounds on values of the decision variables; each element will
            be a tuple containing the lower and upper bound on a decision
            variable.

        If `guess` is provided, `optimizer` must also accept the following
        keyword argument.

        x0 : array_like
            The guesses for each decision variable.

        If the distribution has any shape parameters that must be integral or
        if the distribution is discrete and the location parameter is not
        fixed, `optimizer` must also accept the following keyword argument.

        integrality : array_like of bools
            For each decision variable, True if the decision variable
            must be constrained to integer values and False if the decision
            variable is continuous.

        `optimizer` must return an object, such as an instance of
        `scipy.optimize.OptimizeResult`, which holds the optimal values of
        the decision variables in an attribute ``x``. If attributes
        ``fun``, ``status``, or ``message`` are provided, they will be
        included in the result object returned by `fit`.

    Returns
    -------
    result : `~scipy.stats._result_classes.FitResult`
        An object with the following fields.

        params : namedtuple
            A namedtuple containing the maximum likelihood estimates of the
            shape parameters, location, and (if applicable) scale of the
            distribution.
        success : bool or None
            Whether the optimizer considered the optimization to terminate
            successfully or not.
        message : str or None
            Any status message provided by the optimizer.

        The object has the following method:

        nllf(params=None, data=None)
            By default, the negative log-likelihood function at the fitted
            `params` for the given `data`. Accepts a tuple containing
            alternative shapes, location, and scale of the distribution and
            an array of alternative data.

        plot(ax=None)
            Superposes the PDF/PMF of the fitted distribution over a normalized
            histogram of the data.

    See Also
    --------
    rv_continuous,  rv_discrete

    Notes
    -----
    Optimization is more likely to converge to the maximum likelihood estimate
    when the user provides tight bounds containing the maximum likelihood
    estimate. For example, when fitting a binomial distribution to data, the
    number of experiments underlying each sample may be known, in which case
    the corresponding shape parameter ``n`` can be fixed.

    References
    ----------
    .. [1] Shao, Yongzhao, and Marjorie G. Hahn. "Maximum product of spacings
           method: a unified formulation with illustration of strong
           consistency." Illinois Journal of Mathematics 43.3 (1999): 489-499.

    Examples
    --------
    Suppose we wish to fit a distribution to the following data.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> dist = stats.nbinom
    >>> shapes = (5, 0.5)
    >>> data = dist.rvs(*shapes, size=1000, random_state=rng)

    Suppose we do not know how the data were generated, but we suspect that
    it follows a negative binomial distribution with parameters *n* and *p*\.
    (See `scipy.stats.nbinom`.) We believe that the parameter *n* was fewer
    than 30, and we know that the parameter *p* must lie on the interval
    [0, 1]. We record this information in a variable `bounds` and pass
    this information to `fit`.

    >>> bounds = [(0, 30), (0, 1)]
    >>> res = stats.fit(dist, data, bounds)

    `fit` searches within the user-specified `bounds` for the
    values that best match the data (in the sense of maximum likelihood
    estimation). In this case, it found shape values similar to those
    from which the data were actually generated.

    >>> res.params
    FitParams(n=5.0, p=0.5028157644634368, loc=0.0)  # may vary

    We can visualize the results by superposing the probability mass function
    of the distribution (with the shapes fit to the data) over a normalized
    histogram of the data.

    >>> import matplotlib.pyplot as plt  # matplotlib must be installed to plot
    >>> res.plot()
    >>> plt.show()

    Note that the estimate for *n* was exactly integral; this is because
    the domain of the `nbinom` PMF includes only integral *n*, and the `nbinom`
    object "knows" that. `nbinom` also knows that the shape *p* must be a
    value between 0 and 1. In such a case - when the domain of the distribution
    with respect to a parameter is finite - we are not required to specify
    bounds for the parameter.

    >>> bounds = {'n': (0, 30)}  # omit parameter p using a `dict`
    >>> res2 = stats.fit(dist, data, bounds)
    >>> res2.params
    FitParams(n=5.0, p=0.5016492009232932, loc=0.0)  # may vary

    If we wish to force the distribution to be fit with *n* fixed at 6, we can
    set both the lower and upper bounds on *n* to 6. Note, however, that the
    value of the objective function being optimized is typically worse (higher)
    in this case.

    >>> bounds = {'n': (6, 6)}  # fix parameter `n`
    >>> res3 = stats.fit(dist, data, bounds)
    >>> res3.params
    FitParams(n=6.0, p=0.5486556076755706, loc=0.0)  # may vary
    >>> res3.nllf() > res.nllf()
    True  # may vary

    Note that the numerical results of the previous examples are typical, but
    they may vary because the default optimizer used by `fit`,
    `scipy.optimize.differential_evolution`, is stochastic. However, we can
    customize the settings used by the optimizer to ensure reproducibility -
    or even use a different optimizer entirely - using the `optimizer`
    parameter.

    >>> from scipy.optimize import differential_evolution
    >>> rng = np.random.default_rng(767585560716548)
    >>> def optimizer(fun, bounds, *, integrality):
    ...     return differential_evolution(fun, bounds, strategy='best2bin',
    ...                                   rng=rng, integrality=integrality)
    >>> bounds = [(0, 30), (0, 1)]
    >>> res4 = stats.fit(dist, data, bounds, optimizer=optimizer)
    >>> res4.params
    FitParams(n=5.0, p=0.5015183149259951, loc=0.0)

    """
    # --- Input Validation / Standardization --- #
    user_bounds = bounds
    user_guess = guess

    # distribution input validation and information collection
    if hasattr(dist, "pdf"):  # can't use isinstance for types
        default_bounds = {'loc': (0, 0), 'scale': (1, 1)}
        discrete = False
    elif hasattr(dist, "pmf"):
        default_bounds = {'loc': (0, 0)}
        discrete = True
    else:
        message = ("`dist` must be an instance of `rv_continuous` "
                   "or `rv_discrete.`")
        raise ValueError(message)

    try:
        param_info = dist._param_info()
    except AttributeError as e:
        message = (f"Distribution `{dist.name}` is not yet supported by "
                   "`scipy.stats.fit` because shape information has "
                   "not been defined.")
        raise ValueError(message) from e

    # data input validation
    data = np.asarray(data)
    if data.ndim != 1:
        message = "`data` must be exactly one-dimensional."
        raise ValueError(message)
    if not (np.issubdtype(data.dtype, np.number)
            and np.all(np.isfinite(data))):
        message = "All elements of `data` must be finite numbers."
        raise ValueError(message)

    # bounds input validation and information collection
    n_params = len(param_info)
    n_shapes = n_params - (1 if discrete else 2)
    param_list = [param.name for param in param_info]
    param_names = ", ".join(param_list)
    shape_names = ", ".join(param_list[:n_shapes])

    if user_bounds is None:
        user_bounds = {}

    if isinstance(user_bounds, dict):
        default_bounds.update(user_bounds)
        user_bounds = default_bounds
        user_bounds_array = np.empty((n_params, 2))
        for i in range(n_params):
            param_name = param_info[i].name
            user_bound = user_bounds.pop(param_name, None)
            if user_bound is None:
                user_bound = param_info[i].domain
            user_bounds_array[i] = user_bound
        if user_bounds:
            message = ("Bounds provided for the following unrecognized "
                       f"parameters will be ignored: {set(user_bounds)}")
            warnings.warn(message, RuntimeWarning, stacklevel=2)

    else:
        try:
            user_bounds = np.asarray(user_bounds, dtype=float)
            if user_bounds.size == 0:
                user_bounds = np.empty((0, 2))
        except ValueError as e:
            message = ("Each element of a `bounds` sequence must be a tuple "
                       "containing two elements: the lower and upper bound of "
                       "a distribution parameter.")
            raise ValueError(message) from e
        if (user_bounds.ndim != 2 or user_bounds.shape[1] != 2):
            message = ("Each element of `bounds` must be a tuple specifying "
                       "the lower and upper bounds of a shape parameter")
            raise ValueError(message)
        if user_bounds.shape[0] < n_shapes:
            message = (f"A `bounds` sequence must contain at least {n_shapes} "
                       "elements: tuples specifying the lower and upper "
                       f"bounds of all shape parameters {shape_names}.")
            raise ValueError(message)
        if user_bounds.shape[0] > n_params:
            message = ("A `bounds` sequence may not contain more than "
                       f"{n_params} elements: tuples specifying the lower and "
                       "upper bounds of distribution parameters "
                       f"{param_names}.")
            raise ValueError(message)

        user_bounds_array = np.empty((n_params, 2))
        user_bounds_array[n_shapes:] = list(default_bounds.values())
        user_bounds_array[:len(user_bounds)] = user_bounds

    user_bounds = user_bounds_array
    validated_bounds = []
    for i in range(n_params):
        name = param_info[i].name
        user_bound = user_bounds_array[i]
        param_domain = param_info[i].domain
        integral = param_info[i].integrality
        combined = _combine_bounds(name, user_bound, param_domain, integral)
        validated_bounds.append(combined)

    bounds = np.asarray(validated_bounds)
    integrality = [param.integrality for param in param_info]

    # guess input validation

    if user_guess is None:
        guess_array = None
    elif isinstance(user_guess, dict):
        default_guess = {param.name: np.mean(bound)
                         for param, bound in zip(param_info, bounds)}
        unrecognized = set(user_guess) - set(default_guess)
        if unrecognized:
            message = ("Guesses provided for the following unrecognized "
                       f"parameters will be ignored: {unrecognized}")
            warnings.warn(message, RuntimeWarning, stacklevel=2)
        default_guess.update(user_guess)

        message = ("Each element of `guess` must be a scalar "
                   "guess for a distribution parameter.")
        try:
            guess_array = np.asarray([default_guess[param.name]
                                      for param in param_info], dtype=float)
        except ValueError as e:
            raise ValueError(message) from e

    else:
        message = ("Each element of `guess` must be a scalar "
                   "guess for a distribution parameter.")
        try:
            user_guess = np.asarray(user_guess, dtype=float)
        except ValueError as e:
            raise ValueError(message) from e
        if user_guess.ndim != 1:
            raise ValueError(message)
        if user_guess.shape[0] < n_shapes:
            message = (f"A `guess` sequence must contain at least {n_shapes} "
                       "elements: scalar guesses for the distribution shape "
                       f"parameters {shape_names}.")
            raise ValueError(message)
        if user_guess.shape[0] > n_params:
            message = ("A `guess` sequence may not contain more than "
                       f"{n_params} elements: scalar guesses for the "
                       f"distribution parameters {param_names}.")
            raise ValueError(message)

        guess_array = np.mean(bounds, axis=1)
        guess_array[:len(user_guess)] = user_guess

    if guess_array is not None:
        guess_rounded = guess_array.copy()

        guess_rounded[integrality] = np.round(guess_rounded[integrality])
        rounded = np.where(guess_rounded != guess_array)[0]
        for i in rounded:
            message = (f"Guess for parameter `{param_info[i].name}` "
                       f"rounded from {guess_array[i]} to {guess_rounded[i]}.")
            warnings.warn(message, RuntimeWarning, stacklevel=2)

        guess_clipped = np.clip(guess_rounded, bounds[:, 0], bounds[:, 1])
        clipped = np.where(guess_clipped != guess_rounded)[0]
        for i in clipped:
            message = (f"Guess for parameter `{param_info[i].name}` "
                       f"clipped from {guess_rounded[i]} to "
                       f"{guess_clipped[i]}.")
            warnings.warn(message, RuntimeWarning, stacklevel=2)

        guess = guess_clipped
    else:
        guess = None

    # --- Fitting --- #
    def nllf(free_params, data=data):  # bind data NOW
        with np.errstate(invalid='ignore', divide='ignore'):
            return dist._penalized_nnlf(free_params, data)

    def nlpsf(free_params, data=data):  # bind data NOW
        with np.errstate(invalid='ignore', divide='ignore'):
            return dist._penalized_nlpsf(free_params, data)

    methods = {'mle': nllf, 'mse': nlpsf}
    objective = methods[method.lower()]

    with np.errstate(invalid='ignore', divide='ignore'):
        kwds = {}
        if bounds is not None:
            kwds['bounds'] = bounds
        if np.any(integrality):
            kwds['integrality'] = integrality
        if guess is not None:
            kwds['x0'] = guess
        res = optimizer(objective, **kwds)

    return FitResult(dist, data, discrete, res)

