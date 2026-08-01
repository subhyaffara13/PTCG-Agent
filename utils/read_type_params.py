
def read_type_params(state: State, data: ReadBuffer) -> list[TypeParam]:
    """Read type parameters (PEP 695 generics)."""
    type_params: list[TypeParam] = []
    n = read_int_bare(data)
    for _ in range(n):
        kind = read_int(data)
        name = read_str(data)
        has_bound = read_bool(data)
        if has_bound:
            upper_bound = read_type(state, data)
        else:
            upper_bound = None

        expect_tag(data, LIST_GEN)
        n_values = read_int_bare(data)
        values = [read_type(state, data) for _ in range(n_values)]

        has_default = read_bool(data)
        if has_default:
            default = read_type(state, data)
        else:
            default = None

        type_params.append(TypeParam(name, kind, upper_bound, values, default))

    return type_params

