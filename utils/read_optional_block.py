
def read_optional_block(state: State, data: ReadBuffer) -> Block | None:
    expect_tag(data, nodes.BLOCK)
    expect_tag(data, LIST_GEN)
    n = read_int_bare(data)
    is_unreachable = read_bool(data)
    if n == 0:
        b = None
    else:
        a = [read_statement(state, data) for i in range(n)]
        b = Block(a, is_unreachable=is_unreachable)
        b.line = a[0].line
        b.column = a[0].column
        b.end_line = a[-1].end_line
        b.end_column = a[-1].end_column
    expect_end_tag(data)
    return b

