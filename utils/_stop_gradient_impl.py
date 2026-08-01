
def _stop_gradient_impl(x: T) -> T:
  if not core.valid_jaxtype(x):
    raise TypeError("stop_gradient only works on valid JAX arrays, but "
                    f"input argument is: {x}")
  return x

