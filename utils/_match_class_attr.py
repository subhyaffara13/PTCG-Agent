
def _match_class_attr(obj: object, name: str, seen: set[str]) -> object:
    if name in seen:
        raise TypeError(f"{type(obj)} got multiple sub-patterns for attribute {name}")

    attr = getattr(obj, name)
    seen.add(name)
    return attr

