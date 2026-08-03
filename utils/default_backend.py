from typing import Any

def default_backend() -> str:
  """Returns the platform name of the default XLA backend."""
  return get_backend(None).platform


def default_backend() -> Any:
    from cryptography.hazmat.backends.openssl.backend import backend

    return backend

