
def has_pallas_package() -> bool:
    """Check if Pallas (JAX experimental) is available."""
    if not has_jax_package():
        return False
    try:
        from jax.experimental import (  # noqa: F401  # type: ignore[import-not-found]
            pallas as pl,
        )

        return True
    except ImportError:
        return False

