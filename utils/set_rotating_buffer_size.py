
def set_rotating_buffer_size(buffer_size: int) -> None:
    r"""Set rotating buffer size to this value in MB, if the buffer size is greater than zero.

    If less than zero, query L2 cache size. If equal to zero, means deactivate rotating buffer.
    """
    return torch._C._cuda_tunableop_set_rotating_buffer_size(buffer_size)  # type: ignore[attr-defined]

