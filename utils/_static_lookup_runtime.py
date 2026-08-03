from typing import Any

def _static_lookup_runtime(object_path: list[str]) -> MaybeMissing[Any]:
    static_runtime = importlib.import_module(object_path[0])
    for entry in object_path[1:]:
        try:
            static_runtime = inspect.getattr_static(static_runtime, entry)
        except AttributeError:
            # This can happen with mangled names, ignore for now.
            # TODO: pass more information about ancestors of nodes/objects to verify, so we don't
            # have to do this hacky lookup. Would be useful in several places.
            return MISSING
    return static_runtime

