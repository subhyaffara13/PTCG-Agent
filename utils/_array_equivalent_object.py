
def _array_equivalent_object(
    left: np.ndarray, right: np.ndarray, strict_nan: bool
) -> bool:
    left = ensure_object(left)
    right = ensure_object(right)

    mask: npt.NDArray[np.bool_] | None = None
    if strict_nan:
        mask = isna(left) & isna(right)
        if not mask.any():
            mask = None

    try:
        if mask is None:
            return lib.array_equivalent_object(left, right)
        if not lib.array_equivalent_object(left[~mask], right[~mask]):
            return False
        left_remaining = left[mask]
        right_remaining = right[mask]
    except ValueError:
        # can raise a ValueError if left and right cannot be
        # compared (e.g. nested arrays)
        left_remaining = left
        right_remaining = right

    for left_value, right_value in zip(left_remaining, right_remaining, strict=True):
        if left_value is NaT and right_value is not NaT:
            return False

        elif left_value is libmissing.NA and right_value is not libmissing.NA:
            return False

        elif isinstance(left_value, float) and np.isnan(left_value):
            if not isinstance(right_value, float) or not np.isnan(right_value):
                return False
        else:
            with warnings.catch_warnings():
                # suppress numpy's "elementwise comparison failed"
                warnings.simplefilter("ignore", DeprecationWarning)
                try:
                    if np.any(np.asarray(left_value != right_value)):
                        return False
                except TypeError as err:
                    if "boolean value of NA is ambiguous" in str(err):
                        return False
                    raise
                except ValueError:
                    # numpy can raise a ValueError if left and right cannot be
                    # compared (e.g. nested arrays)
                    return False
    return True

