import math


def entropy(expr, condition=None, **kwargs):
    """
    Calculates entropy of a probability distribution.

    Parameters
    ==========

    expression : the random expression whose entropy is to be calculated
    condition : optional, to specify conditions on random expression
    b: base of the logarithm, optional
       By default, it is taken as Euler's number

    Returns
    =======

    result : Entropy of the expression, a constant

    Examples
    ========

    >>> from sympy.stats import Normal, Die, entropy
    >>> X = Normal('X', 0, 1)
    >>> entropy(X)
    log(2)/2 + 1/2 + log(pi)/2

    >>> D = Die('D', 4)
    >>> entropy(D)
    log(4)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Entropy_%28information_theory%29
    .. [2] https://www.crmarsh.com/static/pdf/Charles_Marsh_Continuous_Entropy.pdf
    .. [3] https://kconrad.math.uconn.edu/blurbs/analysis/entropypost.pdf
    """
    pdf = density(expr, condition, **kwargs)
    base = kwargs.get('b', exp(1))
    if isinstance(pdf, dict):
            return sum(-prob*log(prob, base) for prob in pdf.values())
    return expectation(-log(pdf(expr), base))


def entropy(density):
    """Compute the entropy of a matrix/density object.

    This computes -Tr(density*ln(density)) using the eigenvalue decomposition
    of density, which is given as either a Density instance or a matrix
    (numpy.ndarray, sympy.Matrix or scipy.sparse).

    Parameters
    ==========

    density : density matrix of type Density, SymPy matrix,
    scipy.sparse or numpy.ndarray

    Examples
    ========

    >>> from sympy.physics.quantum.density import Density, entropy
    >>> from sympy.physics.quantum.spin import JzKet
    >>> from sympy import S
    >>> up = JzKet(S(1)/2,S(1)/2)
    >>> down = JzKet(S(1)/2,-S(1)/2)
    >>> d = Density((up,S(1)/2),(down,S(1)/2))
    >>> entropy(d)
    log(2)/2

    """
    if isinstance(density, Density):
        density = represent(density)  # represent in Matrix

    if isinstance(density, scipy_sparse_matrix):
        density = to_numpy(density)

    if isinstance(density, Matrix):
        eigvals = density.eigenvals().keys()
        return expand(-sum(e*log(e) for e in eigvals))
    elif isinstance(density, numpy_ndarray):
        import numpy as np
        eigvals = np.linalg.eigvals(density)
        return -np.sum(eigvals*np.log(eigvals))
    else:
        raise ValueError(
            "numpy.ndarray, scipy.sparse or SymPy matrix expected")


def entropy(pk: np.typing.ArrayLike,
            qk: np.typing.ArrayLike | None = None,
            base: float | None = None,
            axis: int = 0
            ) -> np.number | np.ndarray:
    """
    Calculate the Shannon entropy/relative entropy of given distribution(s).

    If only probabilities `pk` are given, the Shannon entropy is calculated as
    ``H = -sum(pk * log(pk))``.

    If `qk` is not None, then compute the relative entropy
    ``D = sum(pk * log(pk / qk))``. This quantity is also known
    as the Kullback-Leibler divergence.

    This routine will normalize `pk` and `qk` if they don't sum to 1.

    Parameters
    ----------
    pk : array_like
        Defines the (discrete) distribution. Along each axis-slice of ``pk``,
        element ``i`` is the  (possibly unnormalized) probability of event
        ``i``.
    qk : array_like, optional
        Sequence against which the relative entropy is computed. Should be in
        the same format as `pk`.
    base : float, optional
        The logarithmic base to use, defaults to ``e`` (natural logarithm).
    axis : int, optional
        The axis along which the entropy is calculated. Default is 0.

    Returns
    -------
    S : {float, array_like}
        The calculated entropy.

    Notes
    -----
    Informally, the Shannon entropy quantifies the expected uncertainty
    inherent in the possible outcomes of a discrete random variable.
    For example,
    if messages consisting of sequences of symbols from a set are to be
    encoded and transmitted over a noiseless channel, then the Shannon entropy
    ``H(pk)`` gives a tight lower bound for the average number of units of
    information needed per symbol if the symbols occur with frequencies
    governed by the discrete distribution `pk` [1]_. The choice of base
    determines the choice of units; e.g., ``e`` for nats, ``2`` for bits, etc.

    The relative entropy, ``D(pk|qk)``, quantifies the increase in the average
    number of units of information needed per symbol if the encoding is
    optimized for the probability distribution `qk` instead of the true
    distribution `pk`. Informally, the relative entropy quantifies the expected
    excess in surprise experienced if one believes the true distribution is
    `qk` when it is actually `pk`.

    A related quantity, the cross entropy ``CE(pk, qk)``, satisfies the
    equation ``CE(pk, qk) = H(pk) + D(pk|qk)`` and can also be calculated with
    the formula ``CE = -sum(pk * log(qk))``. It gives the average
    number of units of information needed per symbol if an encoding is
    optimized for the probability distribution `qk` when the true distribution
    is `pk`. It is not computed directly by `entropy`, but it can be computed
    using two calls to the function (see Examples).

    See [2]_ for more information.

    References
    ----------
    .. [1] Shannon, C.E. (1948), A Mathematical Theory of Communication.
           Bell System Technical Journal, 27: 379-423.
           :doi:`10.1002/j.1538-7305.1948.tb01338.x`.
    .. [2] Thomas M. Cover and Joy A. Thomas. 2006. Elements of Information
           Theory (Wiley Series in Telecommunications and Signal Processing).
           Wiley-Interscience, USA.


    Examples
    --------
    The outcome of a fair coin is the most uncertain:

    >>> import numpy as np
    >>> from scipy.stats import entropy
    >>> base = 2  # work in units of bits
    >>> pk = np.array([1/2, 1/2])  # fair coin
    >>> H = entropy(pk, base=base)
    >>> H
    1.0
    >>> H == -np.sum(pk * np.log(pk)) / np.log(base)
    True

    The outcome of a biased coin is less uncertain:

    >>> qk = np.array([9/10, 1/10])  # biased coin
    >>> entropy(qk, base=base)
    0.46899559358928117

    The relative entropy between the fair coin and biased coin is calculated
    as:

    >>> D = entropy(pk, qk, base=base)
    >>> D
    0.7369655941662062
    >>> np.isclose(D, np.sum(pk * np.log(pk/qk)) / np.log(base), rtol=4e-16, atol=0)
    True

    The cross entropy can be calculated as the sum of the entropy and
    relative entropy`:

    >>> CE = entropy(pk, base=base) + entropy(pk, qk, base=base)
    >>> CE
    1.736965594166206
    >>> CE == -np.sum(pk * np.log(qk)) / np.log(base)
    True

    """
    if base is not None and base <= 0:
        raise ValueError("`base` must be a positive number or `None`.")

    xp = array_namespace(pk, qk)
    pk, qk = xp_promote(pk, qk, broadcast=True, xp=xp)

    with np.errstate(invalid='ignore'):
        if qk is not None:
            pk, qk = _share_masks(pk, qk, xp=xp)
            qk = qk / xp.sum(qk, axis=axis, keepdims=True)
        pk = pk / xp.sum(pk, axis=axis, keepdims=True)

    if qk is None:
        vec = special.entr(pk)
    else:
        vec = _masked_apply(special.rel_entr, args=(pk, qk), xp=xp)

    S = xp.sum(vec, axis=axis)
    if base is not None:
        S /= math.log(base)
    return S


def entropy(
    pk: np.ndarray,
    qk: np.ndarray,
    base: float | None = None,
    axis: int = 0,
) -> np.ndarray:
    """
    Simplifeied version of entropy.
    Source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html.
    This avoids taking a dependency on scipy just for this function.
    """
    assert base is None or base > 0, "base={base} must be a positive number or `None`."
    assert qk is not None, "qk is None"

    pk = np.asarray(pk).astype(np.float32)
    pk = 1.0 * pk / np.sum(pk, axis=axis, keepdims=True)

    qk = np.asarray(qk).astype(np.float32)
    pk, qk = np.broadcast_arrays(pk, qk)
    qk = 1.0 * qk / np.sum(qk, axis=axis, keepdims=True)
    vec = rel_entr(pk, qk)

    s = np.sum(vec, axis=axis)
    if base is not None:
        s /= np.log(base)
    return s.astype(pk.dtype)


def entropy(mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Shannon entropy of the Poisson distribution.

  JAX implementation of :obj:`scipy.stats.poisson` ``entropy``.

  The entropy :math:`H(X)` of a Poisson random variable
  :math:`X \sim \text{Poisson}(\mu)` is defined as:

  .. math::

   H(X) = -\sum_{k=0}^\infty p(k) \log p(k)

  where :math:`p(k) = e^{-\mu} \mu^k / k!` for
  :math:`k \geq \max(0, \lfloor \text{loc} \rfloor)`.

  This implementation uses **regime switching** for numerical stability
  and performance:

  - **Small** :math:`\mu < 10`: Direct summation over PMF with adaptive
    upper bound :math:`k \leq \mu + 20`
  - **Medium** :math:`10 \leq \mu < 100`: Summation with bound
    :math:`k \leq \mu + 10\sqrt{\mu} + 20`
  - **Large** :math:`\mu \geq 100`: Asymptotic Stirling approximation:
    :math:`H(\mu) \approx \frac{1}{2} \log(2\pi e \mu) - \frac{1}{12\mu}`

  Matches SciPy to relative error :math:`< 10^{-5}` across all regimes.

  Args:
    mu: arraylike, mean parameter of the Poisson distribution.
      Must be ``> 0``.
    loc: arraylike, optional location parameter (default: 0).
      Accepted for API compatibility with scipy but does not
      affect the entropy

  Returns:
    Array of entropy values with shape broadcast from ``mu`` and ``loc``.
    Returns ``NaN`` for ``mu <= 0``.

  Examples:
    >>> from jax.scipy.stats import poisson
    >>> poisson.entropy(5.0)
    Array(2.204394, dtype=float32)
    >>> poisson.entropy(jax.numpy.array([1, 10, 100]))
    Array([1.3048419, 2.561407 , 3.7206903], dtype=float32)

  See Also:
    - :func:`jax.scipy.stats.poisson.cdf`
    - :func:`jax.scipy.stats.poisson.pmf`
    - :func:`jax.scipy.stats.poisson.logpmf`
    - :obj:`scipy.stats.poisson`
  """
  mu, loc = ensure_arraylike("poisson.entropy", mu, loc)
  promoted_mu, promoted_loc = promote_dtypes_inexact(mu, loc)

  #Note: loc does not affect the entropy - translation invariant
  #it has only been taken to maintain compatibility with scipy api
  result_shape = jnp.broadcast_shapes(
    promoted_mu.shape,
    promoted_loc.shape
  )

  mu_flat = jnp.ravel(promoted_mu)
  zero_result = jnp.zeros_like(mu_flat)


  # Choose the computation regime based on mu value
  result = jnp.where(
    mu_flat == 0,
    zero_result,
    jnp.where(
      mu_flat < 10,
      _entropy_small_mu(mu_flat),
      jnp.where(
        mu_flat < 100,
        _entropy_medium_mu(mu_flat),
        _entropy_large_mu(mu_flat)
      )
    )
  )

  result_mu_shape = jnp.reshape(result, promoted_mu.shape)

  # Restore original shape
  return jnp.broadcast_to(result_mu_shape, result_shape)

