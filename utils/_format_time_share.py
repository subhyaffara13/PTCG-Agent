
def _format_time_share(time_us, total_time_us):
    """Define how to format time in FunctionEvent."""
    if total_time_us == 0:
        if time_us != 0:
            raise AssertionError(f"Expected time_us == 0 but got {time_us}")
        return "NaN"
    return f"{time_us * 100.0 / total_time_us:.2f}%"

