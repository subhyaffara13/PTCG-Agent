
def make_class_validator(type_: Type[T]) -> Callable[[Any], Type[T]]:
    def class_validator(v: Any) -> Type[T]:
        if lenient_issubclass(v, type_):
            return v
        raise errors.SubclassError(expected_class=type_)

    return class_validator

