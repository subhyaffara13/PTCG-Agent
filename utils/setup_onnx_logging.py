
def setup_onnx_logging(verbose: bool):
    """A context manager to temporarily set the ONNX logging verbosity.

    .. deprecated:: 2.7
        Please remove usage of this function.
    """
    is_originally_enabled = _C._jit_is_onnx_log_enabled
    if is_originally_enabled or verbose:  # type: ignore[truthy-function]
        _C._jit_set_onnx_log_enabled(True)
    try:
        yield
    finally:
        if not is_originally_enabled:  # type: ignore[truthy-function]
            _C._jit_set_onnx_log_enabled(False)

