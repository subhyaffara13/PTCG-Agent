
def read_statements(state: State, data: ReadBuffer, n: int) -> list[Statement]:
    defs: list[Statement] = []
    old_num_funcs = state.num_funcs
    for _ in range(n):
        stmt = read_statement(state, data)
        defs.append(stmt)
    if state.num_funcs > old_num_funcs + 1:
        # There were at least two functions, so we may need to merge overloads.
        defs = fix_function_overloads(state, defs)
    return defs

