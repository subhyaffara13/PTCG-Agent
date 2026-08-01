
def explicit_device_put_scope() -> Generator[None, None, None]:
  """Indicates that the current context is an explicit device_put*() call."""
  state = guard_lib.thread_local_state()
  prev = state.explicit_device_put
  state.explicit_device_put = True
  try:
    yield
  finally:
    state.explicit_device_put = prev

