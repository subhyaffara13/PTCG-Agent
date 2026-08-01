
def collect_profile(
    port: int,
    duration_in_ms: int,
    host: str,
    log_dir: os.PathLike | str | None,
    no_perfetto_link: bool,
    xprof_options: dict[str, Any] | None = None,):
  options: dict[str, Any] = {
      "host_tracer_level": 2,
      "device_tracer_level": 1,
      "python_tracer_level": 1,
  }
  if xprof_options:
    options.update(xprof_options)

  IS_GCS_PATH = str(log_dir).startswith("gs://")
  log_dir_ = pathlib.Path(log_dir if log_dir is not None else tempfile.mkdtemp())
  str_log_dir = log_dir if IS_GCS_PATH else str(log_dir_)
  _pywrap_profiler_plugin.trace(
      _strip_addresses(f"{host}:{port}", _GRPC_PREFIX),
      str_log_dir,
      '',
      True,
      duration_in_ms,
      DEFAULT_NUM_TRACING_ATTEMPTS,
      options,
  )
  print(f"Dumped profiling information in: {str_log_dir}")
  # Traces stored on GCS cannot be converted to a Perfetto trace, as JAX doesn't
  # directly support GCS paths.
  if IS_GCS_PATH:
    if not no_perfetto_link:
      print("Perfetto link is not supported for GCS paths, skipping creation.")
    return
  # The profiler dumps `xplane.pb` to the logging directory. To upload it to
  # the Perfetto trace viewer, we need to convert it to a `trace.json` file.
  # We do this by first finding the `xplane.pb` file, then passing it into
  # tensorflow_profile_plugin's `xplane` conversion function.
  curr_path = log_dir_.resolve()
  root_trace_folder = curr_path / "plugins" / "profile"
  trace_folders = [root_trace_folder / trace_folder for trace_folder
                   in root_trace_folder.iterdir()]
  latest_folder = max(trace_folders, key=os.path.getmtime)
  xplane = next(latest_folder.glob("*.xplane.pb"))
  result, _ = convert.xspace_to_tool_data([xplane], "trace_viewer", {})

  with gzip.open(str(latest_folder / "remote.trace.json.gz"), "wb") as fp:
    fp.write(result.encode("utf-8"))

  if not no_perfetto_link:
    path = jax_profiler._write_perfetto_trace_file(log_dir_)
    jax_profiler._host_perfetto_trace_file(path)

