
def _meet_fields(types: list[Mapping[str, Type]]) -> Mapping[str, Type]:
    """
    "Meet" the fields of a list of attrs classes, i.e. for each field, its new type will be the lower bound.
    """
    field_to_types = defaultdict(list)
    for fields in types:
        for name, typ in fields.items():
            field_to_types[name].append(typ)

    return {
        name: (
            get_proper_type(reduce(meet_types, f_types))
            if len(f_types) == len(types)
            else UninhabitedType()
        )
        for name, f_types in field_to_types.items()
    }

