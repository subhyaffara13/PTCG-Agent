
def _get_mesh_devices(devices, backend, local_axis_size, axis_size,
                      trace_state_clean):
  """Compute effective mesh devices based on context.

  Args:
    devices: The mesh devices tuple.
    backend: The backend to use.
    local_axis_size: The local axis size (per-process).
    axis_size: User-specified global axis size (optional).
    trace_state_clean: True if in execution mode (not tracing).

  Returns:
    Tuple of effective mesh devices sliced appropriately.

  Raises:
    ValueError: If axis_size doesn't match inferred size in single-process.
  """
  process_count = xb.process_count(backend)

  # Validate explicit axis_size in single-process mode
  if (process_count == 1 and axis_size is not None and
      axis_size != local_axis_size):
    raise ValueError(
        f"Specified axis_size {axis_size} doesn't match received "
        f"axis_size {local_axis_size}.")

  # Compute global_axis_size
  if axis_size is not None:
    global_axis_size = axis_size
  elif process_count > 1:
    global_axis_size = local_axis_size * process_count
    # Validate all processes have the same number of local devices
    assert all(
        len(xb.local_devices(pi, backend)) == xb.local_device_count(backend)
        for pi in range(process_count))
  else:
    global_axis_size = local_axis_size

  # Determine mesh devices
  if devices is not None:
    mesh_devices = devices
  elif process_count > 1:
    # Multi-process: group devices by process (host) for optimal collective
    # performance. This matches the old pmap's device ordering which uses
    # local_devices(process_index) in a nested loop, ensuring devices from
    # the same host are contiguous in the mesh.
    mesh_devices = tuple(
        d
        for process_index in range(process_count)
        for d in xb.local_devices(process_index, backend)
    )
  elif backend is not None:
    mesh_devices = tuple(xb.devices(backend=backend))
  else:
    mesh_devices = tuple(xb.devices())

  if not trace_state_clean and process_count > 1:
    # Tracing in multihost: use local devices
    return tuple(xb.local_devices(backend=backend)[:local_axis_size])
  else:
    return mesh_devices[:global_axis_size]

