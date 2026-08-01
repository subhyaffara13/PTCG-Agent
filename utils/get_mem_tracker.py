
def get_mem_tracker() -> BufferMemoryTracker:
    if local.memory_tracker is None:
        local.memory_tracker = BufferMemoryTracker()
    return local.memory_tracker

