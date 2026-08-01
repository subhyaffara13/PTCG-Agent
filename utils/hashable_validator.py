
def hashable_validator(v: Any) -> Hashable:
    if isinstance(v, Hashable):
        return v

    raise errors.HashableError()

