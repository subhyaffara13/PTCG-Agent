
def _class_getnewargs(obj):
    type_kwargs = {}
    if "__module__" in obj.__dict__:
        type_kwargs["__module__"] = obj.__module__

    __dict__ = obj.__dict__.get("__dict__", None)
    if isinstance(__dict__, property):
        type_kwargs["__dict__"] = __dict__

    return (
        type(obj),
        obj.__name__,
        _get_bases(obj),
        type_kwargs,
        _get_or_create_tracker_id(obj),
        None,
    )

