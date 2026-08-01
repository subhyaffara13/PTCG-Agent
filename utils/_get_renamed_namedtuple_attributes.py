
def _get_renamed_namedtuple_attributes(field_names):
    names = list(field_names)
    seen = set()
    for i, name in enumerate(field_names):
        # pylint: disable = too-many-boolean-expressions
        if (
            not all(c.isalnum() or c == "_" for c in name)
            or keyword.iskeyword(name)
            or not name
            or name[0].isdigit()
            or name.startswith("_")
            or name in seen
        ):
            names[i] = "_%d" % i
        seen.add(name)
    return tuple(names)

