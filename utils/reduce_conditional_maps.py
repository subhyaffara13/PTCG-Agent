
def reduce_conditional_maps(
    type_maps: list[tuple[TypeMap, TypeMap]], use_meet: bool = False
) -> tuple[TypeMap, TypeMap]:
    """Reduces a list containing pairs of if/else TypeMaps into a single pair.

    We "and" together all of the if TypeMaps and "or" together the else TypeMaps. So
    for example, if we had the input:

        [
            ({x: TypeIfX, shared: TypeIfShared1}, {x: TypeElseX, shared: TypeElseShared1}),
            ({y: TypeIfY, shared: TypeIfShared2}, {y: TypeElseY, shared: TypeElseShared2}),
        ]

    ...we'd return the output:

        (
            {x: TypeIfX,   y: TypeIfY,   shared: PseudoIntersection[TypeIfShared1, TypeIfShared2]},
            {shared: Union[TypeElseShared1, TypeElseShared2]},
        )

    ...where "PseudoIntersection[X, Y] == Y" because mypy actually doesn't understand intersections
    yet, so we settle for just arbitrarily picking the right expr's type.

    We only retain the shared expression in the 'else' case because we don't actually know
    whether x was refined or y was refined -- only just that one of the two was refined.
    """
    if len(type_maps) == 0:
        return {}, {}
    elif len(type_maps) == 1:
        return type_maps[0]
    else:
        final_if_map, final_else_map = type_maps[0]
        for if_map, else_map in type_maps[1:]:
            final_if_map = and_conditional_maps(final_if_map, if_map, use_meet=use_meet)
            final_else_map = or_conditional_maps(final_else_map, else_map)

        return final_if_map, final_else_map

