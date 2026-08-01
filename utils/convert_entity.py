
def convert_entity(value):
    """Convert an entity (minus the & and ; part) into what it represents

    This handles numeric, hex, and text entities.

    :arg value: the string (minus the ``&`` and ``;`` part) to convert

    :returns: unicode character or None if it's an ambiguous ampersand that
        doesn't match a character entity

    """
    if value[0] == "#":
        if len(value) < 2:
            return None

        if value[1] in ("x", "X"):
            # hex-encoded code point
            int_as_string, base = value[2:], 16
        else:
            # decimal code point
            int_as_string, base = value[1:], 10

        if int_as_string == "":
            return None

        code_point = int(int_as_string, base)
        if 0 < code_point < 0x110000:
            return chr(code_point)
        else:
            return None

    return ENTITIES.get(value, None)

