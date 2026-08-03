from typing import Any

def check_point_array(points: Any) -> None:
    if not isinstance(points, np.ndarray):
        raise TypeError(f"Expected numpy array not {type(points)}")
    if points.dtype != point_dtype:
        raise ValueError(f"Expected numpy array of dtype {point_dtype} not {points.dtype}")
    if not (points.ndim == 2 and points.shape[1] ==2 and points.shape[0] > 1):
        raise ValueError(f"Expected numpy array of shape (?, 2) not {points.shape}")

