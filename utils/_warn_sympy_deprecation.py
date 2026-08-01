
def _warn_sympy_deprecation(stacklevel=3):
    sympy_deprecation_warning(
        "feature",
        active_deprecations_target="active-deprecations",
        deprecated_since_version="0.0.0",
        stacklevel=stacklevel,
    )

