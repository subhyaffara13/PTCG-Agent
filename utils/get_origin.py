from typing import Any, Optional

def get_origin(v: Any) -> Any:
    pydantic_generic_metadata: PydanticGenericMetadata | None = getattr(v, '__pydantic_generic_metadata__', None)
    if pydantic_generic_metadata:
        return pydantic_generic_metadata.get('origin')
    return typing_extensions.get_origin(v)


def get_origin(tp: type[Any]) -> type[Any] | None:
    return _get_origin(tp)


def get_origin(type_spec: type) -> Optional[type]:   # pylint: disable=g-bare-generic drop when 3.7 support is not needed
  """Call typing.get_origin, with a fallback for Python 3.7 and below."""
  if hasattr(typing, 'get_origin'):
    return typing.get_origin(type_spec)
  return getattr(type_spec, '__origin__', None)

