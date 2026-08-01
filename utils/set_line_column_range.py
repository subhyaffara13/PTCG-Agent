
def set_line_column_range(target: Context, src: Context) -> None:
    target.line = src.line
    target.column = src.column
    target.end_line = src.end_line
    target.end_column = src.end_column

