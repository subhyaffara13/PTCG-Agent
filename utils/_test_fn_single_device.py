
def _test_fn_single_device(arg_0, arg_1):
  tc = unittest.TestCase()
  tc.assertIn(np.shape(arg_0), {(), DEFAULT_NDARRAY_PARAMS_SHAPE})
  tc.assertIn(np.shape(arg_1), {(), DEFAULT_NDARRAY_PARAMS_SHAPE})
  res = DEFAULT_FN(arg_0, arg_1)
  psum_res = jax.lax.psum(res, axis_name='i')
  return psum_res

