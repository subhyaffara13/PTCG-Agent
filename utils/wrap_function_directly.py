
def wrap_function_directly(func: Callable) -> Callable:
    """Wrap a function directly with line_profiler.

    This is the recommended way to profile functions, especially closures or
    functions created dynamically (like wrapper_async in litellm/utils.py).

    Args:
        func: The function to wrap

    Returns:
        The wrapped function that will be profiled when called

    Raises:
        ImportError: If line_profiler is not available
        RuntimeError: If line_profiler cannot be enabled or function cannot be wrapped
    """
    import warnings

    enable_line_profiler()  # Will raise ImportError if not available

    if _line_profiler is None:
        raise RuntimeError("Line profiler was not initialized")

    # Suppress warnings about __wrapped__ - we intentionally want to profile the wrapper
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message=".*__wrapped__.*", category=UserWarning
        )
        # Add function to line_profiler and wrap it
        _line_profiler.add_function(func)
        profiled_function = _line_profiler(func)

    verbose_proxy_logger.info(f"Wrapped function {func.__name__} with line_profiler")
    return profiled_function

