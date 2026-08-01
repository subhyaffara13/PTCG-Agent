
def read_loc(data: ReadBuffer, node: Context) -> None:
    expect_tag(data, LOCATION)
    line = read_int_bare(data)
    node.line = line
    column = read_int_bare(data)
    node.column = column
    node.end_line = line + read_int_bare(data)
    node.end_column = column + read_int_bare(data)

