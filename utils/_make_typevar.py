
def _make_typevar(name, bound, constraints, covariant, contravariant, class_tracker_id):
    tv = typing.TypeVar(
        name,
        *constraints,
        bound=bound,
        covariant=covariant,
        contravariant=contravariant,
    )
    return _lookup_class_or_track(class_tracker_id, tv)

