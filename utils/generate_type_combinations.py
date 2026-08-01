
def generate_type_combinations(types: list[Type]) -> list[Type]:
    """Generate possible combinations of a list of types.

    mypy essentially supports two different ways to do this: joining the types
    and unioning the types. We try both.
    """
    joined_type = join_type_list(types)
    union_type = make_simplified_union(types)
    if joined_type == union_type:
        return [joined_type]
    else:
        return [joined_type, union_type]

