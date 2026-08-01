
def get_class_name_lineno(method) -> tuple[str, int]:
    current_frame = inspect.currentframe()

    # one for the get_class_name call, one for _overload_method call
    for i in range(2):
        if current_frame is None:
            raise AssertionError(f"current_frame is None at iteration {i}")
        current_frame = current_frame.f_back

    if current_frame is None:
        raise AssertionError("current_frame is None after traversing frames")
    class_name = current_frame.f_code.co_name
    line_no = current_frame.f_code.co_firstlineno
    return class_name, line_no

