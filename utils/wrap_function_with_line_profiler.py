from typing import Any

def wrap_function_with_line_profiler(module: Any, function_name: str) -> bool:
    """Dynamically wrap a function with line_profiler.

    Args:
        module: The module containing the function
        function_name: Name of the function to wrap

    Returns:
        True if wrapping was successful, False otherwise
    """
    try:
        enable_line_profiler()  # May raise ImportError if not available
    except ImportError:
        return False

    if _line_profiler is None:
        return False

    try:
        original_function = getattr(module, function_name, None)
        if original_function is None:
            verbose_proxy_logger.warning(
                f"Function {function_name} not found in module {module.__name__}"
            )
            return False

        # Store original function if not already wrapped
        if function_name not in _wrapped_functions:
            _wrapped_functions[function_name] = original_function

        # Wrap with line_profiler
        profiled_function = _line_profiler(original_function)
        setattr(module, function_name, profiled_function)

        verbose_proxy_logger.info(
            f"Wrapped {module.__name__}.{function_name} with line_profiler"
        )
        return True
    except Exception as e:
        verbose_proxy_logger.error(
            f"Error wrapping {function_name} with line_profiler: {e}"
        )
        return False

