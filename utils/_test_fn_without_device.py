
def _test_fn_without_device(arg_0, arg_1):
  tc = unittest.TestCase()
  tc.assertNotIsInstance(arg_0, jax.Array)
  tc.assertNotIsInstance(arg_1, jax.Array)
  return DEFAULT_FN(arg_0, arg_1)

