
def _gamma_one(key: Array, alpha, log_space) -> Array:
  # Ref: A simple method for generating gamma variables, George Marsaglia and Wai Wan Tsang
  # The algorithm can also be founded in:
  # https://en.wikipedia.org/wiki/Gamma_distribution#Generating_gamma-distributed_random_variables
  zero = lax._const(alpha, 0)
  one = lax._const(alpha, 1)
  two = lax._const(alpha, 2)
  minus_one = lax._const(alpha, -1)
  one_over_two = lax._const(alpha, 0.5)
  one_over_three = lax._const(alpha, 1. / 3.)
  squeeze_const = lax._const(alpha, 0.0331)
  dtype = lax.dtype(alpha)

  zero = core.pvary(zero, tuple(core.typeof(alpha).mat.varying))
  one = core.pvary(one, tuple(core.typeof(alpha).mat.varying))
  minus_one = core.pvary(minus_one, tuple(core.typeof(alpha).mat.varying))
  two = core.pvary(two, tuple(core.typeof(alpha).mat.varying))

  # for alpha < 1, we boost alpha to alpha + 1 and get a sample according to
  #   Gamma(alpha) ~ Gamma(alpha+1) * Uniform()^(1 / alpha)
  # When alpha is very small, this boost can be problematic because it may result
  # in floating point underflow; for this reason we compute it in log space if
  # specified by the `log_space` argument:
  #   log[Gamma(alpha)] ~ log[Gamma(alpha + 1)] + log[Uniform()] / alpha
  # Note that log[Uniform()] ~ -Exponential(), but to avoid problems at x=0
  # exponential is computed in terms of log[1 - Uniform()]; we must account for this
  # so that log-space and non-log-space samples match.
  boost_mask = lax.ge(alpha, one)
  alpha_orig = alpha
  alpha = lax.select(boost_mask, alpha, lax.add(alpha, one))

  d = lax.sub(alpha, one_over_three)
  c = lax.div(one_over_three, lax.sqrt(d))

  def _cond_fn(kXVU):
    _, X, V, U = kXVU
    # TODO: use lax.cond when its batching rule is supported
    # The reason is to avoid evaluating second condition which involves log+log
    # if the first condition is satisfied
    cond = lax.bitwise_and(
        lax.ge(U, lax.sub(one, lax.mul(squeeze_const, lax.mul(X, X)))),
        lax.ge(lax.log(U), lax.add(lax.mul(X, one_over_two),
                                   lax.mul(d, lax.add(lax.sub(one, V),
                                                      lax.log(V))))))
    return cond

  def _body_fn(kXVU):
    def _next_kxv(kxv):
      key = kxv[0]
      key, subkey = _split(key)
      x = normal(subkey, (), dtype=dtype)
      v = lax.add(one, lax.mul(x, c))
      return key, x, v

    key = kXVU[0]
    key, x_key, U_key = _split(key, 3)
    _, x, v = lax_control_flow.while_loop(lambda kxv: lax.le(kxv[2], zero),
                                          _next_kxv, (x_key, zero, minus_one))
    X = lax.mul(x, x)
    V = lax.mul(lax.mul(v, v), v)
    U = uniform(U_key, (), dtype=dtype)
    return key, X, V, U

  # initial state is chosen such that _cond_fn will return True
  key, subkey = _split(key)
  _, _, V, _ = lax_control_flow.while_loop(
      _cond_fn, _body_fn, (key, zero, one, two))
  if log_space:
    log_samples = lax.neg(exponential(subkey, (), dtype=dtype))
    log_boost = lax.select(boost_mask | (log_samples == 0), zero,
                           lax.mul(log_samples, lax.div(one, alpha_orig)))
    return lax.add(lax.add(lax.log(d), lax.log(V)), log_boost)
  else:
    samples = 1 - uniform(subkey, (), dtype=dtype)
    boost = lax.select(boost_mask, one,
                       lax.pow(samples, lax.div(one, alpha_orig)))
    return lax.mul(lax.mul(d, V), boost)

