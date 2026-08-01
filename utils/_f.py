
def _f(key, dfnum, dfden, shape, dtype, out_sharding) -> Array:
  dfden = lax.convert_element_type(dfden, dtype)
  dfnum = lax.convert_element_type(dfnum, dtype)
  key_dfd, key_dfn = _split(key)
  chi2_dfn = chisquare(key_dfn, dfnum, shape, dtype, out_sharding=out_sharding)
  chi2_dfd = chisquare(key_dfd, dfden, shape, dtype, out_sharding=out_sharding)
  num = lax.div(chi2_dfn, dfnum)
  den = lax.div(chi2_dfd ,dfden)
  f = lax.div(num, den)
  return f


def _f():
  try: raise
  except Exception:
    from sys import exc_info
    e, er, tb = exc_info()
    return er, tb

