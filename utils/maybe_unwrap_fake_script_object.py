from typing import Any

def maybe_unwrap_fake_script_object(obj: Any) -> Any:
    """If obj is a FakeScriptObject, return the underlying real object."""
    if isinstance(obj, FakeScriptObject):
        return obj.real_obj
    return obj

