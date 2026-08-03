import os
import re

def num_available_amd_gpus(stop_at: int | None = None) -> int:
  """Count AMD GPUs available via KFD kernel driver.

  This function checks for the presence of AMD GPUs by examining KFD kernel
  driver entities as a proxy. In WSL setups, if /dev/dxg exists, this check
  hardcodes the result to 1 GPU for initialization gating. This approach
  provides a good compromise between performance, reliability and simplicity.
  Presence of such entities doesn't guarantee that the GPUs are usable
  through HIP and PJRT, however, we can't do much better without spawning an
  additional process with a potentially complicated setup to run actual HIP
  code. And we don't want to initialize HIP right now inside the current
  process, because doing so might spoil a proper initialization of the
  rocprofiler-sdk later during PJRT startup.

  Args:
    stop_at: If provided, stop counting once this many GPUs are found.
             This allows early exit when only checking for thresholds.

  Returns:
    The number of AMD GPUs detected (up to stop_at if provided).
  """
  try:
    if os.path.exists("/dev/dxg"):
      return 1

    kfd_nodes_path = "/sys/class/kfd/kfd/topology/nodes/"
    if not os.path.exists(kfd_nodes_path):
      return 0

    gpu_count = 0
    # the RE matches strings like "simd_count ##" and extracts the number ##
    r_simd_count = re.compile(r"\bsimd_count\s+(\d+)\b", re.MULTILINE)
    # we're using a non-zero simd_count as a trait of a GPU following the
    # KFD implementation
    # https://github.com/torvalds/linux/blob/ea1013c1539270e372fc99854bc6e4d94eaeff66/drivers/gpu/drm/amd/amdkfd/kfd_topology.c#L941

    for node in os.listdir(kfd_nodes_path):
      node_props_path = os.path.join(kfd_nodes_path, node, "properties")

      if not os.path.exists(node_props_path):
        continue

      try:
        file_size = os.path.getsize(node_props_path)
        # 16KB is more than a reasonable limit
        if file_size <= 0 or file_size > 16 * 1024:
          continue

        with open(node_props_path, "r", encoding="ascii") as f:
          match = r_simd_count.search(f.read())
          if match:
            simd_count = int(match.group(1))
            if simd_count > 0:
              gpu_count += 1
              if stop_at is not None and gpu_count >= stop_at:
                return gpu_count
      except Exception as e:  # pylint: disable=broad-exception-caught
        logger.debug(
          "Failed to read KFD node file '%s': %s", node_props_path, e
        )
        continue

  except Exception as e:  # pylint: disable=broad-exception-caught
    logger.warning("Failed to count AMD GPUs: %s", e)
    return -1
  return gpu_count

