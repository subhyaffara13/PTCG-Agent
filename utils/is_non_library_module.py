
def is_non_library_module(module: str) -> bool:
    """Does module look like a test module or a script?"""
    if module.endswith(
        (
            ".tests",
            ".test",
            ".testing",
            "_tests",
            "_test_suite",
            "test_util",
            "test_utils",
            "test_base",
            ".__main__",
            ".conftest",  # Used by pytest
            ".setup",  # Typically an install script
        )
    ):
        return True
    if module.split(".")[-1].startswith("test_"):
        return True
    if (
        ".tests." in module
        or ".test." in module
        or ".testing." in module
        or ".SelfTest." in module
    ):
        return True
    return False

