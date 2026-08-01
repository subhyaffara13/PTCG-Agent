
def stop_trace():
  """Stops the currently-running profiler trace.

  The trace will be saved to the ``log_dir`` passed to the corresponding
  :func:`start_trace` call. Raises a RuntimeError if a trace hasn't been started.
  """
  with _profile_state.lock:
    profile_session = _profile_state.profile_session
    if profile_session is None:
      raise RuntimeError("No profile started")
    profile_session.stop_and_export(str(_profile_state.log_dir))
    if _profile_state.create_perfetto_trace:
      abs_filename = _write_perfetto_trace_file(str(_profile_state.log_dir))
      if _profile_state.create_perfetto_link:
        _host_perfetto_trace_file(abs_filename)
    _profile_state.reset()
    clear_metadata()

