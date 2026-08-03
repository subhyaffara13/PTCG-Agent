from typing import Union

def safe_squeeze(
    tensor: Union[np.ndarray, "torch.Tensor"], axis: int | None = None
) -> Union[np.ndarray, "torch.Tensor"]:
    """
    Squeezes a tensor, but only if the axis specified has dim 1.
    """
    if axis is None:
        return tensor.squeeze()

    try:
        return tensor.squeeze(axis=axis)
    except ValueError:
        return tensor

