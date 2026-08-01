
def _get_call_stack_info(num_frames: int = 2) -> str:
    """
    Get the function names from the previous 1-2 functions in the call stack.

    Args:
        num_frames: Number of previous frames to include (default: 2)

    Returns:
        A string with format "current_function <- caller_function [<- grandparent_function]"
    """
    try:
        current_frame = inspect.currentframe()
        if current_frame is None:
            return "unknown"

        # Skip this function and the immediate caller (which sets call_type)
        f_back = current_frame.f_back
        if f_back is None:
            return "unknown"
        frame = f_back.f_back
        if frame is None:
            return "unknown"
        function_names = []

        for _ in range(num_frames):
            if frame is None:
                break
            func_name = frame.f_code.co_name
            function_names.append(func_name)
            frame = frame.f_back

        if not function_names:
            return "unknown"

        return " <- ".join(function_names)
    except Exception:
        return "unknown"

