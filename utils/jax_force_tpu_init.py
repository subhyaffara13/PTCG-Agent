import os

def jax_force_tpu_init() -> bool:
  return 'JAX_FORCE_TPU_INIT' in os.environ

