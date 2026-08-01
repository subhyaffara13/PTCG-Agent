
def __array_namespace__(self, *, api_version: None | str = None) -> ModuleType:
  """Return the `Python array API`_ namespace for JAX.

  .. _Python array API: https://data-apis.org/array-api/
  """
  if api_version is not None and api_version != __array_api_version__:
    raise ValueError(f"{api_version=!r} is not available; "
                     f"available versions are: {[__array_api_version__]}")
  import jax.numpy  # pyrefly: ignore[missing-import]
  return jax.numpy

