
def approx_equal(lhs, rhs, tolerance=1e-6):
    return abs(lhs - rhs) <= tolerance * min(lhs, rhs)


def approx_equal(
    quat: Array, other: Array, atol: float | None = None, degrees: bool = False
) -> Array:
    if atol is None:
        if degrees:
            warnings.warn(
                "atol must be set to use the degrees flag, defaulting to 1e-8 radians.",
                stacklevel=2,
            )
        atol = 1e-8
    elif degrees:
        atol = _deg2rad(atol)

    if not broadcastable(quat.shape, other.shape):
        raise ValueError(
            f"Expected broadcastable shapes in both rotations, got {quat.shape[:-1]} "
            f"rotations in first and {other.shape[:-1]} rotations in second object."
        )

    quat_result = compose_quat(other, inv(quat))
    angles = magnitude(quat_result)
    return angles < atol

