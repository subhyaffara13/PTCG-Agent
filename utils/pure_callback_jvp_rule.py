
def pure_callback_jvp_rule(*args, **kwargs):
  del args, kwargs
  raise ValueError(
      "Pure callbacks do not support JVP. "
      "Please use `jax.custom_jvp` to use callbacks while taking gradients.")

