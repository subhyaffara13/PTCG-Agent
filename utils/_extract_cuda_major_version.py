
def _extract_cuda_major_version(version_str: str) -> str:
    """Extract CUDA major version from version string (e.g., '12.1' -> '12').

    Args:
        version_str: CUDA version string to parse

    Returns:
        Major version as string, or "12" if parsing fails
    """
    return version_str.split(".")[0] if version_str else "12"

