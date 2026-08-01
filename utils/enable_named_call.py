
def enable_named_call():
  """Enables named call wrapping for labelling profile traces.

  When named call wrapping is enabled all JAX ops executed in a Module
  will be run under ``jax.named_scope``. The ``Module`` class name will
  show up around the operations belonging to that Module in the
  Tensorboard profiling UI, simplifying the profiling process.

  Note that ``jax.named_scope`` only works for
  compiled functions (e.g.: using jax.jit or jax.pmap).
  """
  global _use_named_call
  _use_named_call = True

