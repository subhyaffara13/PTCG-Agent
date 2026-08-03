from typing import Any, Callable

def resolve_default_value(
    default: Any,
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None,
    *,
    validated_data: dict[str, Any] | None = None,
    call_default_factory: bool = False,
) -> Any:
    """Resolve the default value using either a static default or a default_factory."""
    from ._utils import smart_deepcopy

    if default_factory is None:
        return smart_deepcopy(default)
    if call_default_factory:
        if takes_validated_data_argument(default_factory=default_factory):
            fac = cast('Callable[[dict[str, Any]], Any]', default_factory)
            if validated_data is None:
                raise ValueError(
                    "The default factory requires the 'validated_data' argument, which was not provided when calling 'get_default()'."
                )
            return fac(validated_data)
        else:
            fac = cast('Callable[[], Any]', default_factory)
            return fac()

    return PydanticUndefined

