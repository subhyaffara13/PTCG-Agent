
def linearize_hierarchy(
    info: TypeInfo, obj_type: Callable[[], Instance] | None = None
) -> list[TypeInfo]:
    # TODO describe
    if info.mro:
        return info.mro
    bases = info.direct_base_classes()
    if not bases and info.fullname != "builtins.object" and obj_type is not None:
        # Probably an error, add a dummy `object` base class,
        # otherwise MRO calculation may spuriously fail.
        bases = [obj_type().type]
    lin_bases = []
    for base in bases:
        assert base is not None, f"Cannot linearize bases for {info.fullname} {bases}"
        lin_bases.append(linearize_hierarchy(base, obj_type))
    lin_bases.append(bases)
    return [info] + merge(lin_bases)

