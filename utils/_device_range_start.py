
def _device_range_start(msg: str, stream: int = 0) -> object:
    """
    Marks the start of a range with string message.
    It returns an opaque heap-allocated handle for this range
    to pass to the corresponding call to device_range_end().

    A key difference between this and range_start is that the
    range_start marks the range right away, while _device_range_start
    marks the start of the range as soon as all the tasks on the
    CUDA stream are completed.

    Returns: An opaque heap-allocated handle that should be passed to _device_range_end().

    Args:
        msg (str): ASCII message to associate with the range.
        stream (int): CUDA stream id.
    """
    # pyrefly: ignore [missing-attribute]
    return _nvtx.deviceRangeStart(msg, stream)

