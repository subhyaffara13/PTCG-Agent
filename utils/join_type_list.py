
def join_type_list(types: Sequence[Type]) -> Type:
    if not types:
        # This is a little arbitrary but reasonable. Any empty tuple should be compatible
        # with all variable length tuples, and this makes it possible.
        return UninhabitedType()
    joined = types[0]
    for t in types[1:]:
        joined = join_types(joined, t)
    return joined

