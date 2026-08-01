
def is_cudagraph_capture_sizes(int_key: int | tuple[int, ...]) -> bool:
    """
    Returns true if all dynamic shapes should be captured or the dynamic shape
    int_key should be captured.
    """
    return (
        config.triton.cudagraph_capture_sizes is None
        or int_key in config.triton.cudagraph_capture_sizes
    )

