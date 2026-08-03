from typing import Any

def _get_tensor_bundles(
    header: dict[str, Any], num_hosts: int
) -> list[list[str]]:
  """Partitions tensors in a file into contiguous bundles for each host.

  This method distributes tensors to hosts such that each host reads a
  contiguous block of bytes from the file. It tries to make the total byte
  size read by each host as close to 1/N as possible, where N is the number of
  hosts.

  TODO(b/496270336): Very large tensors should be subdivided among hosts. The
  current approach loads each tensor wholly onto its assigned host. This is
  efficient for checkpoints with lots of small tensors but can cause OOMs for
  very large tensors.

  Args:
    header: The header of the safetensors file.
    num_hosts: The number of hosts.

  Returns:
    A list of lists of tensor names, where each inner list contains the names
    of the tensors assigned to that host.
  """
  # Filter out metadata and sort tensors by their start offset in the file.
  tensors = {k: v for k, v in header.items() if k != "__metadata__"}
  sorted_tensors = sorted(
      tensors.items(), key=lambda item: item[1]["data_offsets"][0]
  )

  if not sorted_tensors:
    return [[] for _ in range(num_hosts)]

  # Calculate total data size based on the last tensor's end offset.
  total_size = sorted_tensors[-1][1]["data_offsets"][1]

  # Greedily assign tensors to hosts.
  bundles = [[] for _ in range(num_hosts)]
  current_bundle = 0
  cumulative_size = 0

  for name, info in sorted_tensors:
    start, end = info["data_offsets"]
    tensor_size = end - start

    if current_bundle < num_hosts - 1:
      # Calculate target cumulative size for current host.
      ideal_cumulative_size = (current_bundle + 1) * (total_size / num_hosts)

      # Decide whether to cut to next host or keep in current bundle.
      dist_if_cut = abs(cumulative_size - ideal_cumulative_size)
      dist_if_keep = abs(
          (cumulative_size + tensor_size) - ideal_cumulative_size
      )

      if dist_if_cut < dist_if_keep and cumulative_size > 0:
        current_bundle += 1

    bundles[current_bundle].append(name)
    cumulative_size += tensor_size

  return bundles

