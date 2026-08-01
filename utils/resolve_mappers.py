
def resolve_mappers(names: Iterable[str]) -> list[AttributeMapper]:
    """Resolve mapper names to instances. Unknown names raise ``ValueError``."""
    out: list[AttributeMapper] = []
    for name in names:
        factory = _MAPPER_BY_NAME.get(name)
        if factory is None:
            raise ValueError(
                f"unknown mapper name {name!r}; known: " f"{sorted(_MAPPER_BY_NAME)}"
            )
        out.append(factory())
    return out

