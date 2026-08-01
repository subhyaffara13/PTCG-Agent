
def meet_type_list(types: list[Type]) -> Type:
    if not types:
        # This should probably be builtins.object but that is hard to get and
        # it doesn't matter for any current users.
        return AnyType(TypeOfAny.implementation_artifact)
    met = types[0]
    for t in types[1:]:
        met = meet_types(met, t)
    return met

