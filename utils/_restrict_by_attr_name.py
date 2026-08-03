import functools
from typing import Callable

def _restrict_by_attr_name(name: str, is_allowed: Callable[[str], bool]):
  """Patch the given backend restriction onto getattr(compiler, name)."""
  inner_backend_compile = getattr(compiler, name)

  @functools.wraps(inner_backend_compile)
  def wrapper(backend, *args, **kwargs):
    if not is_allowed(backend.platform):
      raise RestrictedBackendError(
          f'Compiling a JAX program for {backend.platform} is forbidden by '
          f'restrict_backends().')
    return inner_backend_compile(backend, *args, **kwargs)

  try:
    setattr(compiler, name, wrapper)
    yield
  finally:
    backend_compile = getattr(compiler, name)
    assert backend_compile is wrapper, backend_compile
    setattr(compiler, name, inner_backend_compile)

