
def composite_jvp(*args, **_):
  del args
  raise ValueError(
      "JVP rule for composite not implemented. You can use `jax.custom_jvp` to "
      "add support. See "
      "https://docs.jax.dev/en/latest/_autosummary/jax.custom_jvp.html"
  )

