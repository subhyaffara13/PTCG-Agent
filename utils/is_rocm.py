
def is_rocm() -> bool:
    """Check if we're running on ROCm/HIP platform."""
    return torch.version.hip is not None

