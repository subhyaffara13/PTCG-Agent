
def get_cuda_nonportable_max_cluster_size():
  # Per-device nonportable maximum cluster sizes for Jetson Thor and DGX
  # Spark (GB10) determined by querying cuOccupancyMaxPotentialClusterSize
  if device_kind_match("Thor$"):
    return 8
  elif device_kind_match("GB10$"):
    return 12
  # 16 is the nonportable maximum cluster size on:
  # - Hopper: https://docs.nvidia.com/cuda/hopper-tuning-guide/index.html#:~:text=cluster%20size%20of-,16,-by%20opting%20in
  # - Blackwell: https://docs.nvidia.com/cuda/blackwell-tuning-guide/index.html#:~:text=cluster%20size%20of-,16,-by%20opting%20in
  return 16

