
def get_jax_version(fallback: tuple[int, int, int] = (0, 0, 0)) -> tuple[int, int, int]:
    """Get JAX version as (major, minor, patch) tuple."""
    try:
        import jax  # type: ignore[import-not-found]

        version_parts = jax.__version__.split(".")
        major, minor, patch = (int(v) for v in version_parts[:3])
        return (major, minor, patch)
    except (ImportError, ValueError, AttributeError):
        return fallback

