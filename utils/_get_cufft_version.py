
def _get_cufft_version(cuda_major: str) -> str:
    """Get cufft library version based on CUDA major version.

    Args:
        cuda_major: CUDA major version as string (e.g., "12", "13")

    Returns:
        cufft version as string
    """
    # cufft versions: CUDA 12.x -> 11, CUDA 13.x -> 12
    return "12" if cuda_major == "13" else "11"

