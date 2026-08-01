
def greater_than_validator(x: Any, gt: Any) -> Any:
    try:
        if not (x > gt):
            raise PydanticKnownError('greater_than', {'gt': _safe_repr(gt)})
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'gt' to supplied value {x}")

