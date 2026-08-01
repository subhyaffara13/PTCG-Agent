
def require_torch_large_gpu(test_case, memory: float = 20):
    """Decorator marking a test that requires a CUDA GPU with more than `memory` GiB of memory."""
    if torch_device != "cuda":
        return unittest.skip(reason=f"test requires a CUDA GPU with more than {memory} GiB of memory")(test_case)

    return unittest.skipUnless(
        torch.cuda.get_device_properties(0).total_memory / 1024**3 > memory,
        f"test requires a GPU with more than {memory} GiB of memory",
    )(test_case)

