
def filter_imprecise_kinds(cs: list[Constraint]) -> list[Constraint]:
    """For each ParamSpec remove all imprecise constraints, if at least one precise available."""
    have_precise = set()
    for c in cs:
        if not isinstance(c.origin_type_var, ParamSpecType):
            continue
        if (
            isinstance(c.target, ParamSpecType)
            or isinstance(c.target, Parameters)
            and not c.target.imprecise_arg_kinds
        ):
            have_precise.add(c.type_var)
    new_cs = []
    for c in cs:
        if not isinstance(c.origin_type_var, ParamSpecType) or c.type_var not in have_precise:
            new_cs.append(c)
        if not isinstance(c.target, Parameters) or not c.target.imprecise_arg_kinds:
            new_cs.append(c)
    return new_cs

