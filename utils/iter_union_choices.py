
def iter_union_choices(union_schema: UnionSchema) -> Generator[CoreSchema]:
    """Iterate over the choices of a `'union'` schema."""
    for choice in union_schema['choices']:
        if isinstance(choice, tuple):
            yield choice[0]
        else:
            yield choice

