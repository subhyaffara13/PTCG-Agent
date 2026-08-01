
def _get_failure_dict(
    results: list[T | WRAPPED_EXCEPTION],
) -> dict[int, WRAPPED_EXCEPTION]:
    return cast(
        dict[int, WRAPPED_EXCEPTION],
        {i: err for i, err in enumerate(results) if _is_wrapped_exception(err)},
    )

