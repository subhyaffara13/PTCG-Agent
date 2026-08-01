
def has_jax_package() -> bool:
    """Check if JAX is installed."""
    try:
        import jax  # noqa: F401  # type: ignore[import-not-found]

        return True
    except ImportError:
        return False

