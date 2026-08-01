
def _initialize_memory_usage(
    memory_usage: bool | str | None = None,
) -> bool | str:
    """Get memory usage based on inputs and display options."""
    if memory_usage is None:
        memory_usage = get_option("display.memory_usage")
    return memory_usage

