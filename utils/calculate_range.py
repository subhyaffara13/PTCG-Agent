
def calculate_range(dtype: torch.dtype) -> tuple[float, float]:
    """
    Calculate the range of values for a given torch.dtype.
    Args:
        dtype (torch.dtype): The input dtype.
    Returns:
        tuple: A tuple containing the minimum and maximum values.
    """
    info = torch.finfo(dtype)
    return info.min, info.max

