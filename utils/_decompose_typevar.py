
def _decompose_typevar(obj):
    return (
        obj.__name__,
        obj.__bound__,
        obj.__constraints__,
        obj.__covariant__,
        obj.__contravariant__,
        _get_or_create_tracker_id(obj),
    )

