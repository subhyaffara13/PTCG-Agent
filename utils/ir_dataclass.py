
def ir_dataclass(cls: type[Any] | None = None, /, *, frozen: bool = True) -> Any:
    def wrap(cls: _T) -> _T:
        return dataclasses.dataclass(cls, kw_only=True, frozen=frozen)  # type: ignore[call-overload]

    if cls is None:
        return wrap
    return wrap(cls)

