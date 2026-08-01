
def has_tpu_pallas() -> bool:
    """Checks for a full Pallas-on-TPU environment."""
    return has_pallas_package() and has_jax_tpu_backend() and has_torch_tpu()

