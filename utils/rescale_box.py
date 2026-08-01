
def rescale_box(
    box: Box,
    new_min: np.floating | np.integer | np.ndarray,
    new_max: np.floating | np.integer | np.ndarray,
) -> tuple[Box, Callable[[np.ndarray], np.ndarray], Callable[[np.ndarray], np.ndarray]]:
    """Rescale and shift the given box space to match the given bounds.

    For unbounded components in the original space, the corresponding target bounds must also be infinite and vice versa.

    Args:
        box: The box space to rescale
        new_min: The new minimum bound
        new_max: The new maximum bound

    Returns:
        A tuple containing the rescaled box space, the forward transformation function (original -> rescaled) and the
        backward transformation function (rescaled -> original).
    """
    assert isinstance(box, Box)

    if not isinstance(new_min, np.ndarray):
        assert np.issubdtype(type(new_min), np.integer) or np.issubdtype(
            type(new_min), np.floating
        )
        new_min = np.full(box.shape, new_min)
    assert (
        new_min.shape == box.shape
    ), f"{new_min.shape}, {box.shape}, {new_min}, {box.low}"

    if not isinstance(new_max, np.ndarray):
        assert np.issubdtype(type(new_max), np.integer) or np.issubdtype(
            type(new_max), np.floating
        )
        new_max = np.full(box.shape, new_max)
    assert new_max.shape == box.shape
    assert np.all((new_min == box.low)[np.isinf(new_min) | np.isinf(box.low)])
    assert np.all((new_max == box.high)[np.isinf(new_max) | np.isinf(box.high)])
    assert np.all(new_min <= new_max)
    assert np.all(box.low <= box.high)

    # Imagine the x-axis between the old Box and the y-axis being the new Box
    # float128 is not available everywhere
    try:
        high_low_diff_dtype = np.float128
    except AttributeError:
        high_low_diff_dtype = np.float64

    min_finite = np.isfinite(new_min)
    max_finite = np.isfinite(new_max)
    both_finite = min_finite & max_finite

    high_low_diff = np.array(
        box.high[both_finite], dtype=high_low_diff_dtype
    ) - np.array(box.low[both_finite], dtype=high_low_diff_dtype)

    gradient = np.ones_like(new_min, dtype=box.dtype)
    gradient[both_finite] = (
        new_max[both_finite] - new_min[both_finite]
    ) / high_low_diff

    intercept = np.zeros_like(new_min, dtype=box.dtype)
    # In cases where both are finite, the lower operation takes precedence
    intercept[max_finite] = new_max[max_finite] - box.high[max_finite]
    intercept[min_finite] = (
        gradient[min_finite] * -box.low[min_finite] + new_min[min_finite]
    )

    new_box = Box(
        low=new_min,
        high=new_max,
        shape=box.shape,
        dtype=box.dtype,
    )

    def forward(obs: np.ndarray) -> np.ndarray:
        return gradient * obs + intercept

    def backward(obs: np.ndarray) -> np.ndarray:
        return (obs - intercept) / gradient

    return new_box, forward, backward

