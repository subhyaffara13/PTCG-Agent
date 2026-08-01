
def record_memory_history(
    enabled: str | None = "all", stacks: str = "python", max_entries: int = 0
) -> None:
    r"""Enable/Disable the memory profiler on MTIA allocator

    Args:
        enabled (all or state, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).

        stacks ("python" or "cpp", optional). Select the stack trace to record.

        max_entries (int, optional). Maximum number of entries to record.
    """
    if not is_initialized():
        return
    torch._C._mtia_recordMemoryHistory(enabled, stacks, max_entries)

