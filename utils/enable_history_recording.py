
def enable_history_recording() -> Generator[None, None, None]:
    "Turns on history recording in the CUDA Caching Allocator"
    enabled = torch._C._cuda_isHistoryEnabled()
    try:
        if not enabled:
            torch.cuda.memory._record_memory_history()
        yield
    finally:
        if not enabled:
            torch.cuda.memory._record_memory_history(None)

