
def is_torch_mps_available(min_version: str | None = None) -> bool:
    if is_torch_available():
        import torch

        backend_available = torch.backends.mps.is_available() and torch.backends.mps.is_built()
        if min_version is not None:
            flag = version.parse(get_torch_version()) >= version.parse(min_version)
            backend_available = backend_available and flag
        return backend_available
    return False

