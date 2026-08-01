
def register_subprocess(pid: int, port: int) -> Callable[[], None]:
  """Registers a subprocess's profiler server to be profiled alongside the current process.

  When the current process collects a profile (either programmatically or via
  its profiler server), it will propagate the request to all registered
  subprocesses' profiler servers and subsequently, aggregate all their responses
  into the main response returned by this process's profiler server.

  This is helpful when running workers in separate processes that may affect the
  performance of the main process (e.g. PyGrain).

  NOTE: Currently, only CPU profiling of subprocesses is supported.

  Args:
    pid: The process ID of the subprocess.
    port: The port of the profiler server in the subprocess.

  Returns:
    A function that when called or garbage collected will unregister the
    subprocess from the main process's profiler.

  Raises:
    RuntimeError: If the subprocess fails to be registered (e.g. already
    registered, unable to connect, etc.).
  """
  return _profiler.register_subprocess(pid, port)

