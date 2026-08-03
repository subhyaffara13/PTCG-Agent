from typing import Any

def get_opaque_obj_repr(obj: Any) -> tuple[str, dict[str, type]]:
    """
    Get the FX-evaluable repr for an opaque object and collect required globals.

    Objects must implement __fx_repr__() which should return:
        (repr_string, dict_mapping_name_to_type)

    where repr_string is an evaluable string representation and
    dict_mapping_name_to_type maps the names used in repr_string to their types.

    For example, if repr_string is "Foo(bar=Bar(1))", the dict should be:
        {"Foo": Foo, "Bar": Bar}
    """

    # Enums are special cased
    if isinstance(obj, Enum):
        cls = type(obj)
        return f"{cls.__name__}.{obj.name}", {cls.__name__: cls}

    if not hasattr(obj, "__fx_repr__"):
        raise TypeError(
            f"Value-type opaque object of type {obj} is "
            "expected to have a `__fx_repr__` method "
            "implementation as we will use this to reconstruct "
            "the object in the FX codegen. __fx_repr__ should return "
            "a tuple of (repr_string, dict[str, type])."
        )

    repr_str, globals_dict = obj.__fx_repr__()

    if not isinstance(repr_str, str):
        raise TypeError(
            f"__fx_repr__ for {type(obj).__name__} must return a string as the "
            f"first element, got {type(repr_str).__name__}"
        )

    if not isinstance(globals_dict, dict):
        raise TypeError(
            f"__fx_repr__ for {type(obj).__name__} must return a dict as the "
            f"second element, got {type(globals_dict).__name__}"
        )

    return repr_str, globals_dict

