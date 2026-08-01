
def equality_value_info(t: Type) -> EqualityValueInfo:
    t = get_proper_type(t)
    if isinstance(t, UnionType):
        return combine_equality_value_info(equality_value_info(item) for item in t.items)
    if isinstance(t, TypeVarType):
        if t.values:
            return combine_equality_value_info(equality_value_info(item) for item in t.values)
        return equality_value_info(t.upper_bound)
    if isinstance(t, Instance) and t.last_known_value is not None:
        return equality_value_info(t.last_known_value)
    if isinstance(t, LiteralType):
        return equality_value_info(t.fallback)
    if isinstance(t, Instance):
        if t.type.fullname == "builtins.object":
            return EqualityValueInfo({}, is_top=True)

        enum_type_names = {t.type.fullname} if t.type.is_enum else set()
        domains = {}
        for base in t.type.mro:
            if domain := VALUE_EQUALITY_DOMAINS.get(base.fullname):
                domains[domain] = EqualityDomainInfo({t.type.fullname}, enum_type_names)

        return EqualityValueInfo(domains, is_top=False)
    if isinstance(t, AnyType):
        return EqualityValueInfo({}, is_top=True)
    return EqualityValueInfo({}, is_top=False)

