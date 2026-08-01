
def parse_posix_class(source, info):
    "Parses a POSIX character class."
    negate = source.match("^")
    prop_name, name = parse_property_name(source)
    if not source.match(":]"):
        raise ParseError()

    return lookup_property(prop_name, name, not negate, source, posix=True)

