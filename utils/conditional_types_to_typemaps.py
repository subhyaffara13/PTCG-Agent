
def conditional_types_to_typemaps(
    expr: Expression, yes_type: Type | None, no_type: Type | None
) -> tuple[TypeMap, TypeMap]:
    expr = collapse_walrus(expr)

    yes_map = {} if yes_type is None else {expr: yes_type}
    no_map = {} if no_type is None else {expr: no_type}
    return yes_map, no_map

