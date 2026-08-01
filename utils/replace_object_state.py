
def replace_object_state(
    new: object, old: object, copy_dict: bool = False, skip_slots: tuple[str, ...] = ()
) -> None:
    """Copy state of old node to the new node.

    This handles cases where there is __dict__ and/or attribute descriptors
    (either from slots or because the type is defined in a C extension module).

    Assume that both objects have the same __class__.
    """
    if hasattr(old, "__dict__"):
        if copy_dict:
            new.__dict__ = dict(old.__dict__)
        else:
            new.__dict__ = old.__dict__

    for attr in get_class_descriptors(old.__class__):
        if attr in skip_slots:
            continue
        try:
            if hasattr(old, attr):
                setattr(new, attr, getattr(old, attr))
            elif hasattr(new, attr):
                delattr(new, attr)
        # There is no way to distinguish getsetdescriptors that allow
        # writes from ones that don't (I think?), so we just ignore
        # AttributeErrors if we need to.
        # TODO: What about getsetdescriptors that act like properties???
        except AttributeError:
            pass

