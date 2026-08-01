
def fake_jit(enable_patching: bool = True) -> FakeContext:
  """Context manager for patching `jax.jit` with the identity function.

  This is intended to be used as a debugging tool to programmatically enable or
  disable JIT compilation.

  Can be used either as a context managed scope:

  .. code-block:: python

    with chex.fake_jit():
      @jax.jit
      def foo(x):
        ...

  or by calling `start` and `stop`:

  .. code-block:: python

    fake_jit_context = chex.fake_jit()
    fake_jit_context.start()

    @jax.jit
      def foo(x):
            ...

    fake_jit_context.stop()

  Args:
    enable_patching: Whether to patch `jax.jit`.

  Returns:
    Context where `jax.jit` is patched with the identity function jax is
    configured to avoid jitting internally whenever possible in functions
    such as `jax.lax.scan`, etc.
  """
  stack = FakeContext()
  stack.enter_context(jax.disable_jit(disable=enable_patching))
  return stack

