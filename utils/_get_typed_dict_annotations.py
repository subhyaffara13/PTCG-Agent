from typing import Any

def _get_typed_dict_annotations(schema: type[TypedDictType]) -> dict[str, Any]:
    """Extract type annotations from a TypedDict class."""
    try:
        # Available in Python 3.14+
        import annotationlib

        return annotationlib.get_annotations(schema)
    except ImportError:
        return {
            # We do not use `get_type_hints` here to avoid evaluating ForwardRefs (which might fail).
            # ForwardRefs are not validated by @strict anyway.
            name: value if value is not None else type(None)
            for name, value in schema.__dict__.get("__annotations__", {}).items()
        }

