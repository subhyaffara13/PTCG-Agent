
def lookup_property(property, value, positive, source=None, posix=False, encoding=0):
    "Looks up a property."
    # Normalise the names (which may still be lists).
    property = standardise_name(property) if property else None
    value = standardise_name(value)

    if (property, value) == ("GENERALCATEGORY", "ASSIGNED"):
        property, value, positive = "GENERALCATEGORY", "UNASSIGNED", not positive

    if posix and not property and value.upper() in _POSIX_CLASSES:
        value = 'POSIX' + value

    if property:
        # Both the property and the value are provided.
        prop = PROPERTIES.get(property)
        if not prop:
            if not source:
                raise error("unknown property")

            raise error("unknown property", source.string, source.pos)

        prop_id, value_dict = prop
        val_id = value_dict.get(value)
        if val_id is None:
            if not source:
                raise error("unknown property value")

            raise error("unknown property value", source.string, source.pos)

        return Property((prop_id << 16) | val_id, positive, encoding=encoding)

    # Only the value is provided.
    # It might be the name of a GC, script or block value.
    for property in ("GC", "SCRIPT", "BLOCK"):
        prop_id, value_dict = PROPERTIES.get(property)
        val_id = value_dict.get(value)
        if val_id is not None:
            return Property((prop_id << 16) | val_id, positive, encoding=encoding)

    # It might be the name of a binary property.
    prop = PROPERTIES.get(value)
    if prop:
        prop_id, value_dict = prop
        if set(value_dict) == _BINARY_VALUES:
            return Property((prop_id << 16) | 1, positive, encoding=encoding)

        return Property(prop_id << 16, not positive, encoding=encoding)

    # It might be the name of a binary property starting with a prefix.
    if value.startswith("IS"):
        prop = PROPERTIES.get(value[2 : ])
        if prop:
            prop_id, value_dict = prop
            if "YES" in value_dict:
                return Property((prop_id << 16) | 1, positive, encoding=encoding)

    # It might be the name of a script or block starting with a prefix.
    for prefix, property in (("IS", "SCRIPT"), ("IN", "BLOCK")):
        if value.startswith(prefix):
            prop_id, value_dict = PROPERTIES.get(property)
            val_id = value_dict.get(value[2 : ])
            if val_id is not None:
                return Property((prop_id << 16) | val_id, positive, encoding=encoding)

    # Unknown property.
    if not source:
        raise error("unknown property")

    raise error("unknown property", source.string, source.pos)

