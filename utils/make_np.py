
def make_np(x: torch.Tensor) -> np.ndarray:
    """
    Convert an object into numpy array.

    Args:
      x: An instance of torch tensor

    Returns:
        numpy.array: Numpy array
    """
    if isinstance(x, np.ndarray):
        return x
    if np.isscalar(x):
        return np.array([x])
    if isinstance(x, torch.Tensor):
        if x.device.type == "meta":
            return np.random.randn(1)
        return _prepare_pytorch(x)
    raise NotImplementedError(
        f"Got {type(x)}, but numpy array or torch tensor are expected."
    )

