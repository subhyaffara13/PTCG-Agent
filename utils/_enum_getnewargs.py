
def _enum_getnewargs(obj):
    members = {e.name: e.value for e in obj}
    return (
        obj.__bases__,
        obj.__name__,
        obj.__qualname__,
        members,
        obj.__module__,
        _get_or_create_tracker_id(obj),
        None,
    )

