
def is_nvshmem_used() -> bool:
  return (
      "XLA_FLAGS" in os.environ
      and "--xla_gpu_experimental_enable_nvshmem" in os.environ["XLA_FLAGS"]
  )

