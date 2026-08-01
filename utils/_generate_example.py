
def _generate_example(dist_family):
    n_parameters = dist_family._num_parameters(0)
    shapes = [()] * n_parameters
    rng = np.random.default_rng(615681484984984)
    i = 0
    dist = dist_family._draw(shapes, rng=rng, i_parameterization=i)

    rng = np.random.default_rng(2354873452)
    name = dist_family.__name__
    if n_parameters:
        parameter_names = list(dist._parameterizations[i].parameters)
        parameter_values = [round(getattr(dist, name), 2) for name in
                            parameter_names]
        name_values = [f"{name}={value}" for name, value in
                       zip(parameter_names, parameter_values)]
        instantiation = f"{name}({', '.join(name_values)})"
        attributes = ", ".join([f"X.{param}" for param in dist._parameters])
        X = dist_family(**dict(zip(parameter_names, parameter_values)))
    else:
        instantiation = f"{name}()"
        X = dist

    p = 0.32
    x = round(X.icdf(p), 2)
    y = round(X.icdf(2 * p), 2)  # noqa: F841

    example = f"""
    To use the distribution class, it must be instantiated using keyword
    parameters corresponding with one of the accepted parameterizations.

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> from scipy.stats import {name}
    >>> X = {instantiation}

    For convenience, the ``plot`` method can be used to visualize the density
    and other functions of the distribution.

    >>> X.plot()
    >>> plt.show()

    The support of the underlying distribution is available using the ``support``
    method.

    >>> X.support()
    {X.support()}
    """

    if n_parameters:
        example += f"""
        The numerical values of parameters associated with all parameterizations
        are available as attributes.

        >>> {attributes}
        {tuple(X._parameters.values())}
        """

    example += f"""
    To evaluate the probability density/mass function of the underlying distribution
    at argument ``x={x}``:

    >>> x = {x}
    >>> X.pdf(x), X.pmf(x)
    {X.pdf(x), X.pmf(x)}

    The cumulative distribution function, its complement, and the logarithm
    of these functions are evaluated similarly.

    >>> np.allclose(np.exp(X.logccdf(x)), 1 - X.cdf(x))
    True
    """

    # When two-arg CDF is implemented for DiscreteDistribution, consider removing
    # the special-casing here.
    if issubclass(dist_family, ContinuousDistribution):
        example_continuous = f"""
    The inverse of these functions with respect to the argument ``x`` is also
    available.

    >>> logp = np.log(1 - X.ccdf(x))
    >>> np.allclose(X.ilogcdf(logp), x)
    True

    Note that distribution functions and their logarithms also have two-argument
    versions for working with the probability mass between two arguments. The
    result tends to be more accurate than the naive implementation because it avoids
    subtractive cancellation.

    >>> y = {y}
    >>> np.allclose(X.ccdf(x, y), 1 - (X.cdf(y) - X.cdf(x)))
    True
        """
        example += example_continuous

    example += f"""
    There are methods for computing measures of central tendency,
    dispersion, higher moments, and entropy.

    >>> X.mean(), X.median(), X.mode()
    {X.mean(), X.median(), X.mode()}

    >>> X.variance(), X.standard_deviation()
    {X.variance(), X.standard_deviation()}

    >>> X.skewness(), X.kurtosis()
    {X.skewness(), X.kurtosis()}

    >>> np.allclose(X.moment(order=6, kind='standardized'),
    ...             X.moment(order=6, kind='central') / X.variance()**3)
    True
    """

    # When logentropy is implemented for DiscreteDistribution, remove special-casing
    if issubclass(dist_family, ContinuousDistribution):
        example += """
    >>> np.allclose(np.exp(X.logentropy()), X.entropy())
    True
        """
    else:
        example += f"""
        >>> X.entropy()
        {X.entropy()}
        """

    example += f"""
    Pseudo-random samples can be drawn from
    the underlying distribution using ``sample``.

    >>> X.sample(shape=(4,))
    {repr(X.sample(shape=(4,)))}  # may vary
    """
    # remove the indentation due to use of block quote within function;
    # eliminate blank first line
    example = "\n".join([line.lstrip() for line in example.split("\n")][1:])
    return example

