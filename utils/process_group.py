
def process_group(pg: ProcessGroup) -> Generator[None, None, None]:
    """
    Context manager for process groups. Thread local method.

    Args:
        pg: The process group to use.
    """
    prev_pg = current_process_group()

    _set_process_group(pg)
    try:
        yield
    finally:
        _set_process_group(prev_pg)

