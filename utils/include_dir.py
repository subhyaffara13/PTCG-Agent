import os

def include_dir() -> str:
    """Find the path of the lib-rt dir that needs to be included"""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "lib-rt")


def include_dir() -> str:
  """Get the path to the directory containing header files bundled with jaxlib"""
  # Handle both regular packages (__file__ is set) and namespace packages
  # (__file__ is None but __path__ is available)
  if jaxlib.__file__ is not None:
    jaxlib_dir = os.path.dirname(os.path.abspath(jaxlib.__file__))
  elif hasattr(jaxlib, '__path__') and jaxlib.__path__:
    # For namespace packages, use the first path entry
    jaxlib_dir = jaxlib.__path__[0]
  else:
    raise RuntimeError(
        "Cannot determine jaxlib directory: neither __file__ nor __path__ is available")
  return os.path.join(jaxlib_dir, "include")

