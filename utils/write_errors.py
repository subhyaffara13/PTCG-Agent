
def write_errors(data: WriteBuffer, errs: list[ErrorTuple]) -> None:
    write_tag(data, LIST_GEN)
    write_int_bare(data, len(errs))
    for path, line, column, end_line, end_column, severity, message, code in errs:
        write_tag(data, TUPLE_GEN)
        write_str_opt(data, path)
        write_int(data, line)
        write_int(data, column)
        write_int(data, end_line)
        write_int(data, end_column)
        write_str(data, severity)
        write_str(data, message)
        write_str_opt(data, code)

