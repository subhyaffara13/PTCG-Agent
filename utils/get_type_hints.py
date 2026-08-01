
def get_type_hints(
    obj: Any,
    globalns: dict[str, Any] | None = None,
    localns: Mapping[str, Any] | None = None,
    include_extras: bool = False,
) -> dict[str, Any]:
    return _get_type_hints(obj, globalns=globalns, localns=localns, include_extras=include_extras)

