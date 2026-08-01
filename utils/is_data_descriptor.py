
def is_data_descriptor(obj: object) -> bool:
    """Return True if *obj* is a data descriptor (has __get__ and (__set__ or __delete__))."""
    tp = type(obj)
    if tp in KNOWN_DATA_DESCRIPTOR_TYPES:
        return True
    return hasattr(tp, "__get__") and (
        hasattr(tp, "__set__") or hasattr(tp, "__delete__")
    )

