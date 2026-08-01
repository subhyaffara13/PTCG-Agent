
def stop_and_get_fdo_profile() -> bytes | str:
  """Stops the currently-running profiler trace and export fdo_profile.

  Currently, this is only supported for GPU.
  Raises a RuntimeError if a trace hasn't been started.
  """
  with _profile_state.lock:
    profile_session = _profile_state.profile_session
    if profile_session is None:
      raise RuntimeError("No profile started")
    xspace = profile_session.stop()
    fdo_profile = _profiler.get_fdo_profile(xspace)
    _profile_state.reset()
    clear_metadata()
    return fdo_profile

