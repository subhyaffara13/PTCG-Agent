
def format_frame_info(code: types.CodeType) -> str:
    return (
        f"{getattr(code, 'co_name', '<unknown>')} "
        f"({getattr(code, 'co_filename', '<unknown>')} "
        f"line {getattr(code, 'co_firstlineno', 0)})"
    )

