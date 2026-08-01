
def _initializer_to_method(
  initializer_constructor: tp.Callable[Fargs, jax.nn.initializers.Initializer],
):
  def rngs_initializer_method(
    self: Rngs | RngStream, *args: Fargs.args, **kwargs: Fargs.kwargs
  ) -> KeylessInitializer:
    init_fn = initializer_constructor(*args, **kwargs)

    def rngs_keyless_initializer(*init_args, **init_kwargs):
      return init_fn(self(), *init_args, **init_kwargs)

    return rngs_keyless_initializer

  return rngs_initializer_method

