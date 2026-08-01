
def _enum_getstate(obj):
    clsdict, slotstate = _class_getstate(obj)

    members = {e.name: e.value for e in obj}
    # Cleanup the clsdict that will be passed to _make_skeleton_enum:
    # Those attributes are already handled by the metaclass.
    for attrname in [
        "_generate_next_value_",
        "_member_names_",
        "_member_map_",
        "_member_type_",
        "_value2member_map_",
    ]:
        clsdict.pop(attrname, None)
    for member in members:
        clsdict.pop(member)
        # Special handling of Enum subclasses
    return clsdict, slotstate

