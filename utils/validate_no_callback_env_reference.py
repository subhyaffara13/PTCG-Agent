
def validate_no_callback_env_reference(
    param: str, value: object, *, source: str
) -> None:
    if _is_env_reference(value):
        _raise_env_reference_error(param, source=source)

