
def _to_keyless(
  initializer_constructor: tp.Callable[Fargs, jax.nn.initializers.Initializer],
) -> tp.Callable[Fargs, KeylessInitializer]:
  raise NotImplementedError

