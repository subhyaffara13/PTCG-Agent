
def variants(test_method,
             with_jit: bool = False,
             without_jit: bool = False,
             with_device: bool = False,
             without_device: bool = False,
             with_pmap: bool = False) -> VariantsTestCaseGenerator:
  # pylint: enable=redefined-outer-name
  """Decorates a test to expose Chex variants.

  The decorated test has access to a decorator called ``self.variant``, which
  may be applied to functions to test different JAX behaviors. Consider:

  .. code-block:: python

    @chex.variants(with_jit=True, without_jit=True)
    def test(self):
      @self.variant
      def f(x, y):
        return x + y

      self.assertEqual(f(1, 2), 3)

  In this example, the function ``test`` will be called twice: once with `f`
  jitted (i.e. using `jax.jit`) and another where `f` is not jitted.

  Variants `with_jit=True` and `with_pmap=True` accept additional specific to
  them arguments. Example:

  .. code-block:: python

    @chex.variants(with_jit=True)
    def test(self):
      @self.variant(static_argnums=(1,))
      def f(x, y):
        # `y` is not traced.
        return x + y

      self.assertEqual(f(1, 2), 3)

  Variant `with_pmap=True` also accepts `broadcast_args_to_devices`
  (whether to broadcast each input argument to all participating devices),
  `reduce_fn` (a function to apply to results of pmapped `fn`), and
  `n_devices` (number of devices to use in the `pmap` computation).
  See the docstring of `_with_pmap` for more details (including default values).

  If used with ``absl.testing.parameterized``, `@chex.variants` must wrap it:

  .. code-block:: python

    @chex.variants(with_jit=True, without_jit=True)
    @parameterized.named_parameters('test', *args)
    def test(self, *args):
      ...

  Tests that use this wrapper must be inherited from ``parameterized.TestCase``.
  For more examples see ``variants_test.py``.

  Args:
    test_method: A test method to decorate.
    with_jit: Whether to test with `jax.jit`.
    without_jit: Whether to test without `jax.jit`. Any jit compilation done
      within the test method will not be affected.
    with_device: Whether to test with args placed on device, using
      `jax.device_put`.
    without_device: Whether to test with args (explicitly) not placed on device,
      using `jax.device_get`.
    with_pmap: Whether to test with `jax.pmap`, with computation duplicated
      across devices.

  Returns:
    A decorated ``test_method``.
  """
  return _variants_fn(
      test_method,
      with_jit=with_jit,
      without_jit=without_jit,
      with_device=with_device,
      without_device=without_device,
      with_pmap=with_pmap)

