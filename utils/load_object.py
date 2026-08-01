
def load_object(name: str) -> Any:
    try:
        x = name.split("#")
        if len(x) == 2:
            obj = _load_obj_from_str(x[0])
            val = getattr(obj, x[1])
        else:
            assert len(x) == 1, f"Invalid obj name {name}"
            val = _load_obj_from_str(x[0])
        val = unwrap_if_wrapper(val)
    except (AttributeError, ImportError):
        val = None
    return val

