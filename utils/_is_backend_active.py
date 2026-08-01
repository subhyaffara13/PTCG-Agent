
def _is_backend_active(name, backend):
    if backend.driver.is_active():
        return True
    # Triton may fail to detect the GPU in subprocess workers when using
    # ctypes-based driver detection (triton-lang/triton#9578). Fall back
    # to torch's own device checks which are more reliable in these environments.
    if name == "nvidia":
        import torch

        return torch.cuda.is_available() and torch.version.hip is None
    if name == "amd":
        import torch

        return torch.cuda.is_available() and torch.version.hip is not None
    return False

