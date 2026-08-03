from typing import Any

def unpack_type(tp: Any, /) -> Any | None:
    """Return the type wrapped by the `Unpack` special form, or `None`."""
    return get_args(tp)[0] if typing_objects.is_unpack(get_origin(tp)) else None

