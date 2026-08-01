
def explicit_device_get_scope() -> Generator[None, None, None]:
  """Indicates that the current context is an explicit device_get() call."""
  state = guard_lib.thread_local_state()
  prev = state.explicit_device_get
  state.explicit_device_get = True
  try:
    yield
  finally:
    state.explicit_device_get = prev

