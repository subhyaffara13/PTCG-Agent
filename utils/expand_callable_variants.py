import itertools

def expand_callable_variants(c: CallableType) -> list[CallableType]:
    """Expand a generic callable using all combinations of type variables' values/bounds."""
    for tv in c.variables:
        # We need to expand self-type before other variables, because this is the only
        # type variable that can have other type variables in the upper bound.
        if tv.id.is_self():
            c = expand_type(c, {tv.id: tv.upper_bound}).copy_modified(
                variables=[v for v in c.variables if not v.id.is_self()]
            )
            break

    if not c.is_generic():
        # Fast path.
        return [c]

    tvar_values = []
    for tvar in c.variables:
        if isinstance(tvar, TypeVarType) and tvar.values:
            tvar_values.append(tvar.values)
        else:
            tvar_values.append([tvar.upper_bound])

    variants = []
    for combination in itertools.product(*tvar_values):
        tvar_map = {tv.id: subst for (tv, subst) in zip(c.variables, combination)}
        variants.append(expand_type(c, tvar_map).copy_modified(variables=[]))
    return variants

