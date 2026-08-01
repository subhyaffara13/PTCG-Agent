
def multinomial(
    g: jit_utils.GraphContext, input, num_samples, replacement=False, generator=None
):
    if generator is not None and not symbolic_helper._is_none(generator):
        symbolic_helper._unimplemented(
            "Multinomial", "generator is not supported for multinomial", input
        )
    if not replacement and num_samples > 1:
        symbolic_helper._unimplemented(
            "Multinomial",
            "replacement=False when num_samples > 1 is not supported for multinomial",
            input,
        )

    log_input = log(g, input)
    return g.op(
        "Multinomial",
        log_input,
        dtype_i=_C_onnx.TensorProtoDataType.INT64,
        sample_size_i=num_samples,
    )


def Multinomial(syms, n, *p):
    """
    Creates a discrete random variable with Multinomial Distribution.

    The density of the said distribution can be found at [1].

    Parameters
    ==========

    n : Positive integer
        Represents number of trials
    p : List of event probabilities
        Must be in the range of $[0, 1]$.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import density, Multinomial, marginal_distribution
    >>> from sympy import symbols
    >>> x1, x2, x3 = symbols('x1, x2, x3', nonnegative=True, integer=True)
    >>> p1, p2, p3 = symbols('p1, p2, p3', positive=True)
    >>> M = Multinomial('M', 3, p1, p2, p3)
    >>> density(M)(x1, x2, x3)
    Piecewise((6*p1**x1*p2**x2*p3**x3/(factorial(x1)*factorial(x2)*factorial(x3)),
    Eq(x1 + x2 + x3, 3)), (0, True))
    >>> marginal_distribution(M, M[0])(x1).subs(x1, 1)
    3*p1*p2**2 + 6*p1*p2*p3 + 3*p1*p3**2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Multinomial_distribution
    .. [2] https://mathworld.wolfram.com/MultinomialDistribution.html

    """
    if not isinstance(p[0], list):
        p = (list(p), )
    return multivariate_rv(MultinomialDistribution, syms, n, p[0])


def multinomial(*counts):
    """Number of distinct arrangements of a multiset.

    The expression ``multinomial(3, 4, 2)`` has several equivalent
    interpretations:

    * In the expansion of ``(a + b + c)⁹``, the coefficient of the
      ``a³b⁴c²`` term is 1260.

    * There are 1260 distinct ways to arrange 9 balls consisting of 3 reds, 4
      greens, and 2 blues.

    * There are 1260 unique ways to place 9 distinct objects into three bins
      with sizes 3, 4, and 2.

    The :func:`multinomial` function computes the length of
    :func:`distinct_permutations`.  For example, there are 83,160 distinct
    anagrams of the word "abracadabra":

        >>> from more_itertools import distinct_permutations, ilen
        >>> ilen(distinct_permutations('abracadabra'))
        83160

    This can be computed directly from the letter counts, 5a 2b 2r 1c 1d:

        >>> from collections import Counter
        >>> list(Counter('abracadabra').values())
        [5, 2, 2, 1, 1]
        >>> multinomial(5, 2, 2, 1, 1)
        83160

    A binomial coefficient is a special case of multinomial where there are
    only two categories.  For example, the number of ways to arrange 12 balls
    with 5 reds and 7 blues is ``multinomial(5, 7)`` or ``math.comb(12, 5)``.

    Likewise, factorial is a special case of multinomial where
    the multiplicities are all just 1 so that
    ``multinomial(1, 1, 1, 1, 1, 1, 1) == math.factorial(7)``.

    Reference:  https://en.wikipedia.org/wiki/Multinomial_theorem

    """
    return prod(map(comb, accumulate(counts), counts))


def multinomial(
    key: Array,
    n: RealArray,
    p: RealArray,
    *,
    shape: Shape | None = None,
    dtype: DTypeLikeFloat | None = None,
    unroll: int | bool = 1,
):
  r"""Sample from a multinomial distribution.

  The probability mass function is

  .. math::
      f(x;n,p) = \frac{n!}{x_1! \ldots x_k!} p_1^{x_1} \ldots p_k^{x_k}

  Args:
    key: PRNG key.
    n: number of trials. Should have shape broadcastable to ``p.shape[:-1]``.
    p: probability of each outcome, with outcomes along the last axis.
    shape: optional, a tuple of nonnegative integers specifying the result batch
      shape, that is, the prefix of the result shape excluding the last axis.
      Must be broadcast-compatible with ``p.shape[:-1]``. The default (None)
      produces a result shape equal to ``p.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    unroll: optional, unroll parameter passed to :func:`jax.lax.scan` inside the
      implementation of this function.

  Returns:
    An array of counts for each outcome with the specified dtype and with shape
      ``p.shape`` if ``shape`` is None, otherwise ``shape + (p.shape[-1],)``.
  """

  key, _ = _check_prng_key("multinomial", key)
  check_arraylike("multinomial", n, p)
  n, p = promote_dtypes_inexact(n, p)

  if shape is None:
    shape = p.shape
  n = jnp.broadcast_to(n, shape[:-1])
  p = jnp.broadcast_to(p, shape)

  def f(remainder, ratio_key):
    ratio, key = ratio_key
    count = binomial(key, remainder, ratio.clip(0, 1), dtype=remainder.dtype)
    return remainder - count, count

  p = jnp.moveaxis(p, -1, 0)

  remaining_probs = lax_control_flow.cumsum(p, 0, reverse=True)
  ratios = p / jnp.where(remaining_probs == 0, 1, remaining_probs)

  keys = split(key, ratios.shape[0])
  remainder, counts = lax_control_flow.scan(f, n, (ratios, keys), unroll=unroll)
  # final remainder should be zero

  return jnp.moveaxis(counts, 0, -1).astype(dtype)

