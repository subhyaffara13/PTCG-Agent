
def _get_ue8m0_dtype() -> torch.dtype:
    """Return ``torch.float8_e8m0fnu`` or raise a clear error on torch without FP8 support."""
    if not hasattr(torch, "float8_e8m0fnu"):
        raise RuntimeError(
            "scale_fmt='ue8m0' requires torch.float8_e8m0fnu, which is only available in "
            f"PyTorch >= 2.7 (found {torch.__version__}). Upgrade torch to use UE8M0 FP8 checkpoints."
        )
    return torch.float8_e8m0fnu

