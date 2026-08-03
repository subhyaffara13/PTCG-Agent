from typing import Any, Dict

def create_model_from_namedtuple(namedtuple_cls: Type['NamedTuple'], **kwargs: Any) -> Type['BaseModel']:
    """
    Create a `BaseModel` based on the fields of a named tuple.
    A named tuple can be created with `typing.NamedTuple` and declared annotations
    but also with `collections.namedtuple`, in this case we consider all fields
    to have type `Any`.
    """
    # With python 3.10+, `__annotations__` always exists but can be empty hence the `getattr... or...` logic
    namedtuple_annotations: Dict[str, Type[Any]] = getattr(namedtuple_cls, '__annotations__', None) or {
        k: Any for k in namedtuple_cls._fields
    }
    field_definitions: Dict[str, Any] = {
        field_name: (field_type, Required) for field_name, field_type in namedtuple_annotations.items()
    }
    return create_model(namedtuple_cls.__name__, **kwargs, **field_definitions)

