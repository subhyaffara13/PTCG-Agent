
def _logistic(key, shape, dtype):
  _check_shape("logistic", shape)
  x = uniform(key, shape, dtype, minval=dtypes.finfo(dtype).tiny, maxval=1.)
  return lax.sub(lax.log(x), lax.log1p(lax.neg(x)))


def _logistic(x, accuracy):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  return 1.0 / (1 + lax.exp(-x))

