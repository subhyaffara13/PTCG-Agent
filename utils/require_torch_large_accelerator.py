
def require_torch_large_accelerator(test_case=None, *, memory: float = 20):
    """Decorator marking a test that requires an accelerator with more than `memory` GiB of memory."""

    def memory_decorator(tc):
        if torch_device not in ("cuda", "xpu"):
            return unittest.skip(f"test requires a GPU or XPU with more than {memory} GiB of memory")(tc)

        torch_accel = getattr(torch, torch_device)
        return unittest.skipUnless(
            torch_accel.get_device_properties(0).total_memory / 1024**3 > memory,
            f"test requires a GPU or XPU with more than {memory} GiB of memory",
        )(tc)

    return memory_decorator if test_case is None else memory_decorator(test_case)

