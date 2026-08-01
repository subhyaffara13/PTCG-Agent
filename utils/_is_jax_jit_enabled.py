
def _is_jax_jit_enabled(xp: ModuleType) -> bool:  # numpydoc ignore=PR01,RT01
    """Return True if this function is being called inside ``jax.jit``."""
    import jax  # pylint: disable=import-outside-toplevel

    x = xp.asarray(False)
    try:
        return bool(x)
    except jax.errors.TracerBoolConversionError:
        return True

