
def _xla_gc_callback(*args):
  _jax.collect_garbage()

