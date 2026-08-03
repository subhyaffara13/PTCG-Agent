import functools

def fake_pmap(
    enable_patching: bool = True,
    jit_result: bool = False,
    ignore_axis_index_groups: bool = False,
    fake_parallel_axis: bool = False,
) -> FakeContext:
  """Context manager for patching `jax.pmap` with `jax.vmap`.

  This is intended to be used as a debugging tool to programmatically replace
  pmap transformations with a non-parallel vmap transformation.

  Can be used either as a context managed scope:

  .. code-block:: python

    with chex.fake_pmap():
      @jax.pmap
      def foo(x):
        ...

  or by calling `start` and `stop`:

  .. code-block:: python

    fake_pmap_context = chex.fake_pmap()
    fake_pmap_context.start()
    @jax.pmap
      def foo(x):
        ...
    fake_pmap_context.stop()

  Args:
    enable_patching: Whether to patch `jax.pmap`.
    jit_result: Whether the transformed function should be jitted despite not
      being pmapped.
    ignore_axis_index_groups: Whether to force any parallel operation within the
      context to set `axis_index_groups` to be None. This is a compatibility
      option to allow users of the axis_index_groups parameter to run under the
      fake_pmap context. This feature is not currently supported in vmap, and
      will fail, so we force the parameter to be `None`.
      *Warning*: This will produce different results to running under `jax.pmap`
    fake_parallel_axis: Fake a parallel axis

  Returns:
    Context where `jax.pmap` is patched with `jax.vmap`.
  """
  stack = FakeContext()
  if enable_patching:
    patched_pmap = functools.partial(
        _fake_pmap,
        jit_result=jit_result,
        fake_parallel_axis=fake_parallel_axis)

    stack.enter_context(mock.patch('jax.pmap', patched_pmap))

    if ignore_axis_index_groups:
      stack.enter_context(mock.patch('jax.lax.all_gather', _fake_all_gather))
      stack.enter_context(mock.patch('jax.lax.all_to_all', _fake_all_to_all))
      stack.enter_context(mock.patch('jax.lax.psum', _fake_psum))
      stack.enter_context(mock.patch('jax.lax.pmean', _fake_pmean))
      stack.enter_context(mock.patch('jax.lax.pmax', _fake_pmax))
      stack.enter_context(mock.patch('jax.lax.pmin', _fake_pmin))
      stack.enter_context(mock.patch('jax.lax.pswapaxes', _fake_pswapaxes))
    else:
      # Use default implementations
      pass

  return stack

