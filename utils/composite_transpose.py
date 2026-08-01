
def composite_transpose(*args, **_):
  del args
  raise ValueError(
      "Transpose rule for composite not implemented. You can use"
      "`jax.custom_jvp` or `jax.custom_vjp` to add support. See "
      "https://docs.jax.dev/en/latest/_autosummary/jax.custom_jvp.html"
  )

