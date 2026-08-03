from typing import Any

def check_offset_array(offsets: Any) -> None:
    if not isinstance(offsets, np.ndarray):
        raise TypeError(f"Expected numpy array not {type(offsets)}")
    if offsets.dtype != offset_dtype:
        raise ValueError(f"Expected numpy array of dtype {offset_dtype} not {offsets.dtype}")
    if not (offsets.ndim == 1 and len(offsets) > 1):
        raise ValueError(f"Expected numpy array of shape (?,) not {offsets.shape}")
    if offsets[0] != 0:
        raise ValueError(f"First element of offset array must be 0, not {offsets[0]}")

