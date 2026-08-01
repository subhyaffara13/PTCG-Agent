
def wasserstein_distance(u_values, v_values, u_weights=None, v_weights=None):
    r"""
    Compute the Wasserstein-1 distance between two 1D discrete distributions.

    The Wasserstein distance, also called the Earth mover's distance or the
    optimal transport distance, is a similarity metric between two probability
    distributions [1]_. In the discrete case, the Wasserstein distance can be
    understood as the cost of an optimal transport plan to convert one
    distribution into the other. The cost is calculated as the product of the
    amount of probability mass being moved and the distance it is being moved.
    A brief and intuitive introduction can be found at [2]_.

    .. versionadded:: 1.0.0

    Parameters
    ----------
    u_values : 1d array_like
        A sample from a probability distribution or the support (set of all
        possible values) of a probability distribution. Each element is an
        observation or possible value.

    v_values : 1d array_like
        A sample from or the support of a second distribution.

    u_weights, v_weights : 1d array_like, optional
        Weights or counts corresponding with the sample or probability masses
        corresponding with the support values. Sum of elements must be positive
        and finite. If unspecified, each value is assigned the same weight.

    Returns
    -------
    distance : float
        The computed distance between the distributions.

    Notes
    -----
    Given two 1D probability mass functions, :math:`u` and :math:`v`, the first
    Wasserstein distance between the distributions is:

    .. math::

        l_1 (u, v) = \inf_{\pi \in \Gamma (u, v)} \int_{\mathbb{R} \times
        \mathbb{R}} |x-y| \mathrm{d} \pi (x, y)

    where :math:`\Gamma (u, v)` is the set of (probability) distributions on
    :math:`\mathbb{R} \times \mathbb{R}` whose marginals are :math:`u` and
    :math:`v` on the first and second factors respectively. For a given value
    :math:`x`, :math:`u(x)` gives the probability of :math:`u` at position
    :math:`x`, and the same for :math:`v(x)`.

    If :math:`U` and :math:`V` are the respective CDFs of :math:`u` and
    :math:`v`, this distance also equals to:

    .. math::

        l_1(u, v) = \int_{-\infty}^{+\infty} |U-V|

    See [3]_ for a proof of the equivalence of both definitions.

    The input distributions can be empirical, therefore coming from samples
    whose values are effectively inputs of the function, or they can be seen as
    generalized functions, in which case they are weighted sums of Dirac delta
    functions located at the specified values.

    References
    ----------
    .. [1] "Wasserstein metric", https://en.wikipedia.org/wiki/Wasserstein_metric
    .. [2] Lili Weng, "What is Wasserstein distance?", Lil'log,
           https://lilianweng.github.io/posts/2017-08-20-gan/#what-is-wasserstein-distance.
    .. [3] Ramdas, Garcia, Cuturi "On Wasserstein Two Sample Testing and Related
           Families of Nonparametric Tests" (2015). :arXiv:`1509.02237`.

    See Also
    --------
    wasserstein_distance_nd: Compute the Wasserstein-1 distance between two N-D
        discrete distributions.

    Examples
    --------
    >>> from scipy.stats import wasserstein_distance
    >>> wasserstein_distance([0, 1, 3], [5, 6, 8])
    5.0
    >>> wasserstein_distance([0, 1], [0, 1], [3, 1], [2, 2])
    0.25
    >>> wasserstein_distance([3.4, 3.9, 7.5, 7.8], [4.5, 1.4],
    ...                      [1.4, 0.9, 3.1, 7.2], [3.2, 3.5])
    4.0781331438047861

    """
    return _cdf_distance(1, u_values, v_values, u_weights, v_weights)

