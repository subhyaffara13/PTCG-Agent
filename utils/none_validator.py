
def none_validator(v: Any) -> 'Literal[None]':
    if v is None:
        return v
    raise errors.NotNoneError()

