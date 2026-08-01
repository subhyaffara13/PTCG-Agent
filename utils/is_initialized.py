
def is_initialized() -> bool:
    r"""Returns True if the CPU is initialized. Always True.

    N.B. This function only exists to facilitate device-agnostic code
    """
    return True


def is_initialized():
    r"""Return whether PyTorch's CUDA state has been initialized."""
    return _initialized and not _is_in_bad_fork()


def is_initialized() -> bool:
    """Check if the default process group has been initialized."""
    return GroupMember.WORLD is not None


def is_initialized():
    r"""Return whether PyTorch's MTIA state has been initialized."""
    return _initialized and not _is_in_bad_fork()


def is_initialized():
    r"""Return whether PyTorch's XPU state has been initialized."""
    return _initialized and not _is_in_bad_fork()


def is_initialized() -> bool:
  """
  Deprecated.

  Return whether the cache is enabled. Initialization can be deferred, so
  initialized status is not checked. The name is retained for backwards
  compatibility.
  """
  return _is_cache_enabled()


def is_initialized() -> bool:
  """Check if the JAX distributed system is initialized."""
  return global_state.client is not None

