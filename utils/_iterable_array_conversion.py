from typing import Any

def _iterable_array_conversion(
    value: Iterable[Any], xp: ModuleType, device: Device | None = None
) -> Iterable[Any]:
    """Convert an Iterable from Arrays to an iterable of the specified xp module array type."""
    # There is currently no type for ArrayAPI compatible objects, so they fall through to this
    # function registered for any Iterable. If they are arrays, we can convert them directly.
    # We currently cannot pass the device to the from_dlpack function, since it is not supported
    # for some frameworks (see e.g. https://github.com/data-apis/array-api-compat/issues/204)
    if is_array_api_obj(value):
        return _array_api_array_conversion(value, xp, device)
    if hasattr(value, "_make"):
        # namedtuple - underline used to prevent potential name conflicts
        # noinspection PyProtectedMember
        return type(value)._make(array_conversion(v, xp, device) for v in value)
    return type(value)(array_conversion(v, xp, device) for v in value)

