
def _check_runtime_available() -> tuple[bool, Version | None]:
    """
    Check if cutedsl (and deps) are available.

    NOTE: Doesn't import at this point
    """
    # Skip all checks if running on CPU-only binary
    if not _cuda.is_built():
        return (False, None)

    deps = [
        ("nvidia_cutlass_dsl", "cutlass"),
        ("apache_tvm_ffi", "tvm_ffi"),
    ]
    reason = _unavailable_reason(deps)
    if reason is None:
        available = True
        version = _available_version("nvidia_cutlass_dsl")
    else:
        log.warning(
            "CuTeDSL operators require optional Python packages "
            "`nvidia-cutlass-dsl` and `apache-tvm-ffi`; "
            "%s",
            reason,
        )
        available = False
        version = None
    return available, version


def _check_runtime_available() -> tuple[bool, Version | None]:
    """
    Check if triton is available

    NOTE: must not import at this point
    """
    # Skip all checks if running on CPU-only binary
    if not _cuda.is_built():
        return (False, None)

    deps = [
        ("triton", "triton"),
    ]
    reason = _unavailable_reason(deps)
    if reason is None:
        available = True
        version = _available_version("triton")
    else:
        log.warning("triton native DSL ops require: `triton` %s", reason)
        available = False
        version = None
    return available, version

