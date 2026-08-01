
def check_pydantic_core_version() -> bool:
    """Check that the installed `pydantic-core` dependency is compatible."""
    return __pydantic_core_version__ == _COMPATIBLE_PYDANTIC_CORE_VERSION

