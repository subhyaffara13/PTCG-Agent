
def _enum_has_attribute(
    owner: astroid.Instance | nodes.ClassDef, node: nodes.Attribute
) -> bool:
    if isinstance(owner, astroid.Instance):
        enum_def = next(
            (b.parent for b in owner.bases if isinstance(b.parent, nodes.ClassDef)),
            None,
        )

        if enum_def is None:
            # We don't inherit from anything, so try to find the parent
            # class definition and roll with that
            enum_def = node
            while enum_def is not None and not isinstance(enum_def, nodes.ClassDef):
                enum_def = enum_def.parent

        # If this blows, something is clearly wrong
        assert enum_def is not None, "enum_def unexpectedly None"
    else:
        enum_def = owner

    # Find __new__ and __init__
    dunder_new = next((m for m in enum_def.methods() if m.name == "__new__"), None)
    dunder_init = next((m for m in enum_def.methods() if m.name == "__init__"), None)

    enum_attributes: set[str] = set()

    # Find attributes defined in __new__
    if dunder_new:
        # Get the object returned in __new__
        returned_obj_name = next(
            (c.value for c in dunder_new.get_children() if isinstance(c, nodes.Return)),
            None,
        )
        if isinstance(returned_obj_name, nodes.Name):
            # Find all attribute assignments to the returned object
            enum_attributes |= _get_all_attribute_assignments(
                dunder_new, returned_obj_name.name
            )

    # Find attributes defined in __init__
    if dunder_init and dunder_init.body and dunder_init.args:
        # Grab the name referring to `self` from the function def
        enum_attributes |= _get_all_attribute_assignments(
            dunder_init, dunder_init.args.arguments[0].name
        )

    return node.attrname in enum_attributes

