import os

def start_trace(
    log_dir: os.PathLike | str,
    create_perfetto_link: bool = False,
    create_perfetto_trace: bool = False,
    profiler_options: ProfileOptions | None = None,
) -> None:
  """Starts a profiler trace.

  The trace will capture CPU, GPU, and/or TPU activity, including Python
  functions and JAX on-device operations. Use :func:`stop_trace` to end the
  trace
  and save the results to ``log_dir``.

  The resulting trace can be viewed with TensorBoard. Note that TensorBoard
  doesn't need to be running when collecting the trace.

  Only one trace may be collected at a time. A RuntimeError will be raised if
  :func:`start_trace` is called while another trace is running.

  Args:
    log_dir: The directory to save the profiler trace to (usually the
      TensorBoard log directory).
    create_perfetto_link: A boolean which, if true, creates and prints link to
      the Perfetto trace viewer UI (https://ui.perfetto.dev). The program will
      block until the link is opened and Perfetto loads the trace.
    create_perfetto_trace: A boolean which, if true, additionally dumps a
      ``perfetto_trace.json.gz`` file that is compatible for upload with the
      Perfetto trace viewer UI (https://ui.perfetto.dev). The file will also be
      generated if ``create_perfetto_link`` is true. This could be useful if you
      want to generate a Perfetto-compatible trace without blocking the process.
    profiler_options: Profiler options to configure the profiler for collection.
  """
  with _profile_state.lock:
    if _profile_state.profile_session is not None:
      raise RuntimeError("Profile has already been started. "
                         "Only one profile may be run at a time.")
    clear_metadata()
    # Make sure backends are initialized before creating a profiler
    # session. Otherwise on Cloud TPU, libtpu may not be initialized before
    # creating the tracer, which will cause the TPU tracer initialization to
    # fail and no TPU operations will be included in the profile.
    xla_bridge.get_backend()

    options = profiler_options
    if options is None:
      options = ProfileOptions()
    set_metadata("jax_version", jax_version_module.__version__)
    jaxlib_version_str = ".".join(map(str, version_lib))
    set_metadata("jaxlib_version", jaxlib_version_str)
    for backend_name in xla_bridge.backends():
      try:
        backend = xla_bridge.get_backend(backend_name)
        set_metadata(f"{backend.platform}_version", backend.platform_version)
      except RuntimeError:
        pass
    _profile_state.profile_session = _profiler.ProfilerSession(options)
    _profile_state.create_perfetto_link = create_perfetto_link
    _profile_state.create_perfetto_trace = (
        create_perfetto_trace or create_perfetto_link)
    _profile_state.log_dir = str(log_dir)

