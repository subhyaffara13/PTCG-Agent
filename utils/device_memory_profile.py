
def device_memory_profile(backend: str | None = None) -> bytes:
  """Captures a JAX device memory profile as ``pprof``-format protocol buffer.

  A device memory profile is a snapshot of the state of memory, that describes the JAX
  :class:`~jax.Array` and executable objects present in memory and their
  allocation sites.

  For more information how to use the device memory profiler, see
  :doc:`/device_memory_profiling`.

  The profiling system works by instrumenting JAX on-device allocations,
  capturing a Python stack trace for each allocation. The instrumentation is
  always enabled; :func:`device_memory_profile` provides an API to capture it.

  The output of :func:`device_memory_profile` is a binary protocol buffer that
  can be interpreted and visualized by the `pprof tool
  <https://github.com/google/pprof>`_.

  Args:
    backend: optional; the name of the JAX backend for which the device memory
      profile should be collected.

  Returns:
    A byte string containing a binary `pprof`-format protocol buffer.
  """
  client = xla_bridge.get_backend(backend)
  return gzip.compress(client.heap_profile())

