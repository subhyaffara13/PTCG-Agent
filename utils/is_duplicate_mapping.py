
def is_duplicate_mapping(
    mapping: list[int], actual_types: list[Type], actual_kinds: list[ArgKind]
) -> bool:
    return (
        len(mapping) > 1
        # Multiple actuals can map to the same formal if they both come from
        # varargs (*args and **kwargs); in this case at runtime it is possible
        # that here are no duplicates. We need to allow this, as the convention
        # f(..., *args, **kwargs) is common enough.
        and not (
            len(mapping) == 2
            and actual_kinds[mapping[0]] == nodes.ARG_STAR
            and actual_kinds[mapping[1]] == nodes.ARG_STAR2
        )
        # Multiple actuals can map to the same formal if there are multiple
        # **kwargs which cannot be mapped with certainty (non-TypedDict
        # **kwargs).
        and not all(
            actual_kinds[m] == nodes.ARG_STAR2
            and not isinstance(get_proper_type(actual_types[m]), TypedDictType)
            for m in mapping
        )
    )

