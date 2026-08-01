
def parse_property_name(source):
    "Parses a property name, which may be qualified."
    name = source.get_while(PROPERTY_NAME_PART)
    saved_pos = source.pos

    ch = source.get()
    if ch and ch in ":=":
        prop_name = name
        name = source.get_while(ALNUM | set(" &_-./")).strip()

        if name:
            # Name after the ":" or "=", so it's a qualified name.
            saved_pos = source.pos
        else:
            # No name after the ":" or "=", so assume it's an unqualified name.
            prop_name, name = None, prop_name
    else:
        prop_name = None

    source.pos = saved_pos
    return prop_name, name

