
def namedtuple_args_cls(schema):
    attribs = [arg.name for arg in schema.arguments.flat_all]
    name = str(schema.name) + "_args"
    # mypy doesn't support dynamic namedtuple name
    tuple_cls = namedtuple(name, attribs)  # type: ignore[misc]
    return tuple_cls

