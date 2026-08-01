
def _check_pyarrow_available() -> None:
    if not HAS_PYARROW:
        msg = (
            f"pyarrow>={PYARROW_MIN_VERSION} is required for PyArrow "
            "backed ArrowExtensionArray."
        )
        raise ImportError(msg)

