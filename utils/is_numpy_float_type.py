
def is_numpy_float_type(value: Any) -> bool:
    if not np:
        return False

    return istype(
        value,
        (
            np.float16,
            np.float32,
            np.float64,
        ),
    )

