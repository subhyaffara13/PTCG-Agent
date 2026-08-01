
def has_pallas() -> bool:
    """
    Check if Pallas backend is fully available for use.

    Requirements:
    - JAX package installed
    - Pallas (jax.experimental.pallas) available
    - A compatible backend (CUDA or TPU) is available in both PyTorch and JAX.
    """
    return has_cpu_pallas() or has_cuda_pallas() or has_tpu_pallas()

