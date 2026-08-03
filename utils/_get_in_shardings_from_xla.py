import os

def _get_in_shardings_from_xla(
    xla_executable, device_list: xc.DeviceList, num_in_avals: int,
    num_ordered_effects: int
  ) -> Sequence[GSPMDSharding] | None:
  """Returns input shardings from XLA."""
  # When the device assignment only has 1 device, SPMD partitioner will not run.
  # Hence the op shardings will not be set on the `hlo_module`.
  assert isinstance(device_list, xc.DeviceList)
  if len(device_list) == 1:
    return [GSPMDSharding.get_replicated(device_list)] * num_in_avals

  in_op_shardings, _ = get_op_sharding_from_executable(xla_executable)
  if not in_op_shardings:
    return None

  if num_ordered_effects > 0:
    in_op_shardings = in_op_shardings[num_ordered_effects:]

  assert len(in_op_shardings) == num_in_avals, (
      len(in_op_shardings), num_in_avals)

  return [GSPMDSharding(device_list, os) for os in in_op_shardings]

