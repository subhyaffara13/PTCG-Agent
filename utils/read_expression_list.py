
def read_expression_list(state: State, data: ReadBuffer) -> list[Expression]:
    expect_tag(data, LIST_GEN)
    n = read_int_bare(data)
    return [read_expression(state, data) for i in range(n)]

