
def _from_numpy_array(array: np.ndarray) -> torch.Tensor:
    """Convert a NumPy array to a PyTorch tensor."""
    import ml_dtypes  # type: ignore[import-not-found]
    import numpy as np

    if array.dtype == ml_dtypes.bfloat16:
        return torch.from_numpy(array.view(np.uint16)).view(torch.bfloat16)
    if array.dtype == ml_dtypes.float8_e4m3fn:
        return torch.from_numpy(array.view(np.uint8)).view(torch.float8_e4m3fn)
    if array.dtype == ml_dtypes.float8_e4m3fnuz:
        return torch.from_numpy(array.view(np.uint8)).view(torch.float8_e4m3fnuz)
    if array.dtype == ml_dtypes.float8_e5m2:
        return torch.from_numpy(array.view(np.uint8)).view(torch.float8_e5m2)
    if array.dtype == ml_dtypes.float8_e5m2fnuz:
        return torch.from_numpy(array.view(np.uint8)).view(torch.float8_e5m2fnuz)
    return torch.from_numpy(array)

