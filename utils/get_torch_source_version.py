
def get_torch_source_version() -> str:
    """Return the source commit hash for the current PyTorch build."""
    import torch.version as torch_version

    return getattr(torch_version, "git_version", "")

