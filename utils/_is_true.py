
def _is_true(value: str | None) -> bool:
    if value is None:
        return False
    return value.upper() in ENV_VARS_TRUE_VALUES

