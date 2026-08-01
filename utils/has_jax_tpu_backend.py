
def has_jax_tpu_backend() -> bool:
    """Check if JAX has TPU backend support."""
    if not has_jax_package():
        return False
    try:
        import jax  # type: ignore[import-not-found]

        # Check if TPU backend is available
        devices = jax.devices("tpu")
        return len(devices) > 0
    except Exception:
        return False

