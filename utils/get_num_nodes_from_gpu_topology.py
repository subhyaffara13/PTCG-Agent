
def get_num_nodes_from_gpu_topology(topology: str) -> int:
    try:
      slices_str, hosts_per_slice_str, _ = topology.split("x", 2)
      return int(slices_str) * int(hosts_per_slice_str)
    except (IndexError, ValueError):
      raise ValueError('Mock topology must be of the form '
                       '"<number-of-slices> x <number-of-hosts-per-slice> x '
                       '<number-of-devices-per-host>".')

