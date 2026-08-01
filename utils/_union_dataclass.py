
def _union_dataclass(cls: type[T]) -> type[T]:
    if not issubclass(cls, _Union):
        raise AssertionError(f"{cls} must inherit from {_Union}.")
    return dataclass(repr=False, eq=False)(cls)

