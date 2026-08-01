
def _buffer_callback_transpose_rule(*args, **kwargs):
  del args, kwargs
  raise ValueError(
      "Buffer callbacks do not support transpose. "
      "Please use `jax.custom_vjp` to use callbacks while taking gradients.")

