from typing import Any

def find_fake_class(full_qualname) -> Any | None:
    if not has_fake_class(full_qualname):
        return None
    return global_fake_class_registry.get_impl(full_qualname)

