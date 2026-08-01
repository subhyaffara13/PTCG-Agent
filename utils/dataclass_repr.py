
def dataclass_repr(
    obj: Any,
    indent: int = 0,
    width: int = 80,
) -> str:
    return pformat(obj, indent, width)

