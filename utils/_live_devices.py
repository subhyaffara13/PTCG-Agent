
def _live_devices(client, devices: list[xla_client.Device]) -> dict[xla_client.Device, int]:
  """Returns the subset of the provided devices that are live and healthy."""
  process_ids = {d.process_index for d in devices}
  if xla_bridge.process_index() not in process_ids:
    # A process can only participate in an live_devices call if it hosts some of
    # the provided devices.
    raise ValueError('Provided devices do not have any local devices.')

  live_process_ids = client.get_live_nodes(list(process_ids))
  return {
      d: live_process_ids[d.process_index]
      for d in devices
      if d.process_index in live_process_ids
  }

