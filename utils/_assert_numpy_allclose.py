
def _assert_numpy_allclose(a, b, atol=None, rtol=None, err_msg=''):
  if a.dtype == b.dtype == _dtypes.float0:
    np.testing.assert_array_equal(a, b, err_msg=err_msg)
    return

  custom_float_dtypes = [
    _dtypes.float4_e2m1fn,
    _dtypes.float8_e8m0fnu,
    _dtypes.float8_e3m4,
    _dtypes.float8_e4m3,
    _dtypes.float8_e4m3b11fnuz,
    _dtypes.float8_e4m3fn,
    _dtypes.float8_e4m3fnuz,
    _dtypes.float8_e5m2,
    _dtypes.float8_e5m2fnuz,
    _dtypes.bfloat16,
  ]

  def maybe_upcast(x):
    if x.dtype in custom_float_dtypes:
      return x.astype(np.float32)
    # TODO(reedwm): Upcasting int2/int4 to int8 will no longer be necessary once
    # JAX depends on a version of ml_dtypes which contains
    # https://github.com/jax-ml/ml_dtypes/commit/348fd3704306cae97f617c38045cee6bc416bf10.
    if x.dtype in _dtypes._intn_dtypes:
      return x.astype(np.int8 if _dtypes.iinfo(x.dtype).min < 0 else np.uint8)
    return x

  a = maybe_upcast(a)
  b = maybe_upcast(b)

  kw = {}
  if atol: kw["atol"] = atol
  if rtol: kw["rtol"] = rtol
  with np.errstate(invalid='ignore'):
    # TODO(phawkins): surprisingly, assert_allclose sometimes reports invalid
    # value errors. It should not do that.
    np.testing.assert_allclose(a, b, **kw, err_msg=err_msg)

