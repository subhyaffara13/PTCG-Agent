
def _test_fn_with_device(arg_0, arg_1):
  tc = unittest.TestCase()
  tc.assertIsInstance(arg_0, jax.Array)
  tc.assertIsInstance(arg_1, jax.Array)
  return DEFAULT_FN(arg_0, arg_1)

