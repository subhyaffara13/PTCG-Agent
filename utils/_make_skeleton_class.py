
def _make_skeleton_class(
    type_constructor, name, bases, type_kwargs, class_tracker_id, extra
):
    """Build dynamic class with an empty __dict__ to be filled once memoized

    If class_tracker_id is not None, try to lookup an existing class definition
    matching that id. If none is found, track a newly reconstructed class
    definition under that id so that other instances stemming from the same
    class id will also reuse this class definition.

    The "extra" variable is meant to be a dict (or None) that can be used for
    forward compatibility shall the need arise.
    """
    # We need to intern the keys of the type_kwargs dict to avoid having
    # different pickles for the same dynamic class depending on whether it was
    # dynamically created or reconstructed from a pickled stream.
    type_kwargs = {sys.intern(k): v for k, v in type_kwargs.items()}

    skeleton_class = types.new_class(
        name, bases, {"metaclass": type_constructor}, lambda ns: ns.update(type_kwargs)
    )

    return _lookup_class_or_track(class_tracker_id, skeleton_class)

