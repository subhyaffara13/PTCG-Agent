
def _descriptor_shape_fits_in_int32(
    sizes: Sequence[sympy.Expr], add_guards: bool = False
) -> bool:
    int32_max = torch.iinfo(torch.int32).max
    conditions = []
    for size in sizes:
        if isinstance(size, (int, sympy.Integer)):
            if size > int32_max:
                return False
        else:
            conditions.append(sympy.Le(size, int32_max))

    if not conditions:
        return True

    from .virtualized import V

    condition = conditions[0] if len(conditions) == 1 else sympy.And(*conditions)
    return (
        V.graph.sizevars.guard_or_false(condition)
        if add_guards
        else V.graph.sizevars.statically_known_true(condition)
    )

