
def inside_call_tf():
  # Set the inside_call_tf flag for a context.
  prev = _thread_local_state.inside_call_tf
  _thread_local_state.inside_call_tf = True
  try:
    yield
  finally:
    _thread_local_state.inside_call_tf = prev

