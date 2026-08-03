import os

def get_out_shardings_from_executable(
    xla_executable,
    device_list: xc.DeviceList,
    num_out_avals: int,
    num_ordered_effects: int,
) -> Sequence[sharding_impls.GSPMDSharding] | None:
  assert isinstance(device_list, xc.DeviceList)

  try:
    omk = xla_executable.get_output_memory_kinds()[0]
    if num_ordered_effects > 0:
      omk = omk[num_ordered_effects:]
  except:
    omk = [None] * num_out_avals

  assert len(omk) == num_out_avals, (len(omk), num_out_avals)

  # When the device assignment only has 1 device, SPMD partitioner will not run.
  # Hence the op shardings will not be set on the `hlo_module`.
  if len(device_list) == 1:
    return [sharding_impls.GSPMDSharding.get_replicated(device_list, memory_kind=mk)
            for mk in omk]

  out_op_shardings: Sequence[xc.OpSharding]
  _, out_op_shardings = get_op_sharding_from_executable(xla_executable)
  if not out_op_shardings:
    return None

  if num_ordered_effects > 0:
    out_op_shardings = out_op_shardings[num_ordered_effects:]

  # This means that there are no outputs for JAX but for XLA there is an empty
  # tuple output which gets a replicated sharding.
  if num_out_avals == 0 and len(out_op_shardings) == 1:
    return None

  # This condition happens when all the elements in the output tuple have the
  # same sharding, so XLA decides to run the `FusionTupleDeduplicator` to
  # put the sharding on ROOT instead of the tuple.
  # TODO(b/245667823): Remove this when XLA fixes this.
  if len(out_op_shardings) == 1 and len(out_op_shardings) < num_out_avals:
    out_op_shardings = list(out_op_shardings) * num_out_avals

  assert len(out_op_shardings) == num_out_avals == len(omk), (
      len(out_op_shardings), num_out_avals, len(omk))

  return [sharding_impls.GSPMDSharding(device_list, os, memory_kind=mk)
          for os, mk in safe_zip(out_op_shardings, omk)]

