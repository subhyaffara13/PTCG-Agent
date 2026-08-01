
def any_class_validator(v: Any) -> Type[T]:
    if isinstance(v, type):
        return v
    raise errors.ClassError()

