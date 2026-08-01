
def _device_range_end(range_handle: object, stream: int = 0) -> None:
    """
    Mark the end of a range for a given range_handle as soon as all the tasks
    on the CUDA stream are completed.

    Args:
        range_handle: an unique handle for the start range.
        stream (int): CUDA stream id.
    """
    # pyrefly: ignore [missing-attribute]
    _nvtx.deviceRangeEnd(range_handle, stream)

