
def require_cuda_capability_at_least(major, minor):
    """Decorator: when running on CUDA, skip if device capability is below the given
    threshold. On non-CUDA backends this is a no-op — pair with :func:`require_torch_gpu`
    if the test is CUDA-only, or leave alone if it should also run on other backends
    (which won't be capability-gated)."""
    import torch

    if not torch.cuda.is_available():
        return lambda test_case: test_case
    capability = torch.cuda.get_device_capability()
    return unittest.skipIf(capability < (major, minor), f"Requires CUDA capability >= {major}.{minor}")

