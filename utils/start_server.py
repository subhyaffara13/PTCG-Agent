import sys

def start_server(args: argparse.Namespace, allow_sources: bool = False) -> None:
    """Start the server from command arguments and wait for it."""
    # Lazy import so this import doesn't slow down other commands.
    from mypy.dmypy_server import daemonize, process_start_options

    start_options = process_start_options(args.flags, allow_sources)
    if daemonize(start_options, args.status_file, timeout=args.timeout, log_file=args.log_file):
        sys.exit(2)
    wait_for_server(args.status_file)


def start_server(
    port: int, requires_backend: bool = True
) -> _profiler.ProfilerServer:
  """Starts the profiler server on port `port`.

  Using the "TensorFlow profiler" feature in `TensorBoard
  <https://www.tensorflow.org/tensorboard>`_ 2.2 or newer, you can
  connect to the profiler server and sample execution traces that show CPU,
  GPU, and/or TPU device activity.

  Args:
    port: The port to start the profiler server on.
    requires_backend: If False, the profiler server will not wait for backends
      to be initialized before starting. Default is True.
  """
  global _profiler_server
  if _profiler_server is not None:
    raise ValueError("Only one profiler server can be active at a time.")

  # Make sure backends are initialized before creating a profiler
  # session. Otherwise on Cloud TPU, libtpu may not be initialized before
  # creating the tracer, which will cause the TPU tracer initialization to
  # fail and no TPU operations will be included in the profile.
  # NOTE(skyewm): I'm not sure this is necessary for start_server (is definitely
  # is for start_trace), but I'm putting it here to be safe.
  if requires_backend:
    xla_bridge.get_backend()

  _profiler_server = _profiler.start_server(port)
  return _profiler_server

