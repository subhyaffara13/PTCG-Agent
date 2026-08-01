
def _assert_numpy_close(a, b, atol=None, rtol=None, err_msg=''):
  a, b = np.asarray(a), np.asarray(b)
  assert a.shape == b.shape
  atol = max(tolerance(a.dtype, atol), tolerance(b.dtype, atol))
  rtol = max(tolerance(a.dtype, rtol), tolerance(b.dtype, rtol))
  _assert_numpy_allclose(a, b, atol=atol * a.size, rtol=rtol * b.size,
                         err_msg=err_msg)

