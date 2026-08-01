
def has_triton_package() -> bool:
    try:
        import triton  # noqa: F401

        return True
    except ImportError:
        return False

