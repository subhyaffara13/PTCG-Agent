
def forbid_inf_nan_check(x: Any) -> Any:
    if not math.isfinite(x):
        raise PydanticKnownError('finite_number')
    return x

