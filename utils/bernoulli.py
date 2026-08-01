
def bernoulli(
    self: torch.Tensor,
    *,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    if generator is None:
        raw_p = torch.rand(self.size(), dtype=torch.float32, device=self.device)
    else:
        raw_p = torch.rand(
            self.size(),
            generator=generator,
            dtype=torch.float32,
            device=self.device,
        )
    p = (raw_p < self).to(self.dtype)
    return p


def bernoulli(g: jit_utils.GraphContext, input, p=None, generator=None, out=None):
    if out is not None and not symbolic_helper._is_none(out):
        symbolic_helper._unimplemented(
            "Bernoulli", "out parameter is not supported for bernoulli", input
        )
    if generator is not None and not symbolic_helper._is_none(generator):
        symbolic_helper._unimplemented(
            "Bernoulli", "generator is not supported for bernoulli", input
        )
    if p is None or symbolic_helper._is_none(p):
        return g.op("Bernoulli", input)
    return opset9.bernoulli(g, input, p, generator, out)


def bernoulli(g: jit_utils.GraphContext, input, p=None, generator=None, out=None):
    if out is not None and not symbolic_helper._is_none(out):
        symbolic_helper._unimplemented(
            "Bernoulli", "out parameter is not supported for bernoulli", input
        )
    if generator is not None and not symbolic_helper._is_none(generator):
        symbolic_helper._unimplemented(
            "Bernoulli", "generator is not supported for bernoulli", input
        )

    dtype = _type_utils.JitScalarType.from_value(
        input, _type_utils.JitScalarType.UNDEFINED
    )
    if dtype == _type_utils.JitScalarType.UNDEFINED:
        return symbolic_helper._unimplemented(
            "Bernoulli", "input dtype not accessible", input
        )

    rands = g.op(
        "RandomUniformLike",
        input,
        high_f=1.0,
        low_f=0.0,
        dtype_i=dtype.onnx_type(),
    )
    prob = p if p is not None and not symbolic_helper._is_none(p) else input
    output = g.op("Less", rands, prob)
    return g.op("Cast", output, to_i=dtype.onnx_type())


def Bernoulli(name, p, succ=1, fail=0):
    r"""
    Create a Finite Random Variable representing a Bernoulli process.

    Parameters
    ==========

    p : Rational number between 0 and 1
       Represents probability of success
    succ : Integer/symbol/string
       Represents event of success
    fail : Integer/symbol/string
       Represents event of failure

    Examples
    ========

    >>> from sympy.stats import Bernoulli, density
    >>> from sympy import S

    >>> X = Bernoulli('X', S(3)/4) # 1-0 Bernoulli variable, probability = 3/4
    >>> density(X).dict
    {0: 1/4, 1: 3/4}

    >>> X = Bernoulli('X', S.Half, 'Heads', 'Tails') # A fair coin toss
    >>> density(X).dict
    {Heads: 1/2, Tails: 1/2}

    Returns
    =======

    RandomSymbol

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bernoulli_distribution
    .. [2] https://mathworld.wolfram.com/BernoulliDistribution.html

    """

    return rv(name, BernoulliDistribution, p, succ, fail)


def bernoulli(n):
    """Bernoulli numbers B0..Bn (inclusive).

    Parameters
    ----------
    n : int
        Indicated the number of terms in the Bernoulli series to generate.

    Returns
    -------
    ndarray
        The Bernoulli numbers ``[B(0), B(1), ..., B(n)]``.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html
    .. [2] "Bernoulli number", Wikipedia, https://en.wikipedia.org/wiki/Bernoulli_number

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import bernoulli, zeta
    >>> bernoulli(4)
    array([ 1.        , -0.5       ,  0.16666667,  0.        , -0.03333333])

    The Wikipedia article ([2]_) points out the relationship between the
    Bernoulli numbers and the zeta function, ``B_n^+ = -n * zeta(1 - n)``
    for ``n > 0``:

    >>> n = np.arange(1, 5)
    >>> -n * zeta(1 - n)
    array([ 0.5       ,  0.16666667, -0.        , -0.03333333])

    Note that, in the notation used in the wikipedia article,
    `bernoulli` computes ``B_n^-`` (i.e. it used the convention that
    ``B_1`` is -1/2).  The relation given above is for ``B_n^+``, so the
    sign of 0.5 does not match the output of ``bernoulli(4)``.

    """
    if not isscalar(n) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    n = int(n)
    if (n < 2):
        n1 = 2
    else:
        n1 = n
    return _specfun.bernob(int(n1))[:(n+1)]


def bernoulli(key: ArrayLike,
              p: RealArray = 0.5,
              shape: Shape | None = None,
              mode: str = 'low',
              *,
              out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Bernoulli random values with given shape and mean.

  The values are distributed according to the probability mass function:

  .. math::
     f(k; p) = p^k(1 - p)^{1 - k}

  where :math:`k \in \{0, 1\}` and :math:`0 \le p \le 1`.

  Args:
    key: a PRNG key used as the random key.
    p: optional, a float or array of floats for the mean of the random
      variables. Must be broadcast-compatible with ``shape``. Default 0.5.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Must be broadcast-compatible with ``p.shape``. The default (None)
      produces a result shape equal to ``p.shape``.
    mode: optional, "high" or "low" for how many bits to use when sampling.
      default='low'. Set to "high" for correct sampling at small values of
      `p`. When sampling in float32, bernoulli samples with mode='low' produce
      incorrect results for p < ~1E-7. mode="high" approximately doubles the
      cost of sampling.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with boolean dtype and shape given by ``shape`` if ``shape``
    is not None, or else ``p.shape``.
  """
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  if mode not in ['high', 'low']:
    raise ValueError(f"got {mode=}, expected 'high' or 'low'")
  key, _ = _check_prng_key("bernoulli", key)
  out_sharding = canonicalize_sharding(out_sharding, "bernoulli")
  dtype = lax.dtype(p)
  if not dtypes.issubdtype(dtype, np.floating):
    msg = "bernoulli probability `p` must have a floating dtype, got {}."
    raise TypeError(msg.format(dtype))
  p = lax.convert_element_type(p, dtype)
  return maybe_auto_axes(_bernoulli, out_sharding,
                         shape=shape, mode=mode)(key, p)


def bernoulli(n: int) -> Array:
  """Generate the first N Bernoulli numbers.

  JAX implementation of :func:`scipy.special.bernoulli`.

  Args:
    n: integer, the number of Bernoulli terms to generate.

  Returns:
    Array containing the first ``n`` Bernoulli numbers.

  Notes:
    ``bernoulli`` generates numbers using the :math:`B_n^-` convention,
    such that :math:`B_1=-1/2`.
  """
  # Generate Bernoulli numbers using the Chowla and Hartung algorithm.
  n = core.concrete_or_error(operator.index, n, "Argument n of bernoulli")
  if n < 0:
    raise ValueError("n must be a non-negative integer.")
  b3 = jnp.array([1, -1/2, 1/6])
  if n < 3:
    return b3[:n + 1]
  bn = jnp.zeros(n + 1).at[:3].set(b3)
  m = jnp.arange(4, n + 1, 2, dtype=bn.dtype)
  q1 = (1. / np.pi ** 2) * jnp.cumprod(-(m - 1) * m / 4 / np.pi ** 2)
  k = jnp.arange(2, 50, dtype=bn.dtype)  # Choose 50 because 2 ** -50 < 1E-15
  q2 = jnp.sum(k[:, None] ** -m[None, :], axis=0)
  return bn.at[4::2].set(q1 * (1 + q2))

