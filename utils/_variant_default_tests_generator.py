import itertools

def _variant_default_tests_generator(fn, is_jit_context, which_variants,
                                     **var_kwargs):
  """Returns a generator with standard tests.

  For internal usage. Allows to dynamically generate common tests.
  See tests' names and comments for more information.

  Args:
    fn: a separate function to be tested (without `self` argument).
    is_jit_context: is a function is supposed to be JIT-ted.
    which_variants: chex variants to use in tests generation.
    **var_kwargs: kwargs for variants wrappers.

  Returns:
    A generator with tests.
  """

  # All generated tests use default arguments (defined at the top of this file).
  arg_0, arg_1, expected = DEFAULT_PARAMS[0]
  varg_0, varg_1, vexpected = (
      _scalar_to_ndarray(a) for a in (arg_0, arg_1, expected))

  # We test whether the function has been jitted by introducing a counter
  # variable as a side-effect. When the function is repeatedly called, jitted
  # code will only execute the side-effect once
  python_execution_count = 0

  def fn_with_counter(*args, **kwargs):
    nonlocal python_execution_count
    python_execution_count += 1
    return fn(*args, **kwargs)

  def exec_with_tracing_counter_checks(self, var_fn, arg_0, arg_1):
    self.assertEqual(python_execution_count, 0)
    _ = var_fn(arg_0, arg_1)
    # In jit context, JAX can omit retracing a function from the previous
    # test, hence `python_execution_count` will be equal to 0.
    # In non-jit context, `python_execution_count` must always increase.
    if not is_jit_context:
      self.assertEqual(python_execution_count, 1)
    actual = var_fn(arg_0, arg_1)
    if is_jit_context:
      # Either 1 (initial tracing) or 0 (function reuse).
      self.assertLess(python_execution_count, 2)
    else:
      self.assertEqual(python_execution_count, 2)
    return actual

  # Here, various tests follow. Tests' names intended to be self-descriptive.
  @variants.variants(**which_variants)
  def test_with_scalar_args(self):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, arg_0, arg_1)
    self.assertEqual(actual, expected)

  @variants.variants(**which_variants)
  def test_called_variant(self):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(**var_kwargs)(fn_with_counter)
    actual = exec_with_tracing_counter_checks(self, var_fn, arg_0, arg_1)
    self.assertEqual(actual, expected)

  @variants.variants(**which_variants)
  def test_with_kwargs(self):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(
        self, var_fn, arg_1=arg_1, arg_0=arg_0)
    self.assertEqual(actual, expected)

  @variants.variants(**which_variants)
  @parameterized.parameters(*DEFAULT_PARAMS)
  def test_scalar_parameters(self, arg_0, arg_1, expected):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, arg_0, arg_1)
    self.assertEqual(actual, expected)

  @variants.variants(**which_variants)
  @parameterized.named_parameters(*DEFAULT_NAMED_PARAMS)
  def test_named_scalar_parameters(self, arg_0, arg_1, expected):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, arg_0, arg_1)
    self.assertEqual(actual, expected)

  @variants.variants(**which_variants)
  def test_with_ndarray_args(self):
    nonlocal python_execution_count
    python_execution_count = 0
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, varg_0, varg_1)
    vexpected_ = vexpected
    # pmap variant case.
    if len(actual.shape) == len(DEFAULT_NDARRAY_PARAMS_SHAPE) + 1:
      vexpected_ = jnp.broadcast_to(vexpected_, actual.shape)
    np.testing.assert_array_equal(actual, vexpected_)

  @variants.variants(**which_variants)
  @parameterized.parameters(*DEFAULT_PARAMS)
  def test_ndarray_parameters(self, arg_0, arg_1, expected):
    nonlocal python_execution_count
    python_execution_count = 0
    varg_0, varg_1, vexpected = (
        _scalar_to_ndarray(a) for a in (arg_0, arg_1, expected))
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, varg_0, varg_1)
    # pmap variant case.
    if len(actual.shape) == len(DEFAULT_NDARRAY_PARAMS_SHAPE) + 1:
      vexpected = jnp.broadcast_to(vexpected, actual.shape)
    np.testing.assert_array_equal(actual, vexpected)

  @variants.variants(**which_variants)
  @parameterized.named_parameters(*DEFAULT_NAMED_PARAMS)
  def test_ndarray_named_parameters(self, arg_0, arg_1, expected):
    nonlocal python_execution_count
    python_execution_count = 0
    varg_0, varg_1, vexpected = (
        _scalar_to_ndarray(a) for a in (arg_0, arg_1, expected))
    var_fn = self.variant(fn_with_counter, **var_kwargs)
    actual = exec_with_tracing_counter_checks(self, var_fn, varg_0, varg_1)
    # pmap variant case.
    if len(actual.shape) == len(DEFAULT_NDARRAY_PARAMS_SHAPE) + 1:
      vexpected = jnp.broadcast_to(vexpected, actual.shape)
    np.testing.assert_array_equal(actual, vexpected)

  all_tests = (test_with_scalar_args, test_called_variant, test_with_kwargs,
               test_scalar_parameters, test_named_scalar_parameters,
               test_with_ndarray_args, test_ndarray_parameters,
               test_ndarray_named_parameters)

  # Each test is a generator itself, hence we use chaining from itertools.
  return itertools.chain(*all_tests)

