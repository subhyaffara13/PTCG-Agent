
def fake_pmap_and_jit(enable_pmap_patching: bool = True,
                      enable_jit_patching: bool = True) -> FakeContext:
  """Context manager for patching `jax.jit` and `jax.pmap`.

  This is a convenience function, equivalent to nested `chex.fake_pmap` and
  `chex.fake_jit` contexts.

  Note that calling (the true implementation of) `jax.pmap` will compile the
  function, so faking `jax.jit` in this case will not stop the function from
  being compiled.

  Args:
    enable_pmap_patching: Whether to patch `jax.pmap`.
    enable_jit_patching: Whether to patch `jax.jit`.

  Returns:
    Context where jax.pmap and jax.jit are patched with jax.vmap and the
    identity function
  """
  stack = FakeContext()
  stack.enter_context(fake_pmap(enable_pmap_patching))
  stack.enter_context(fake_jit(enable_jit_patching))
  return stack

