
def get_statement_startend2(lineno: int, node: ast.AST) -> tuple[int, int | None]:
    # Flatten all statements and except handlers into one lineno-list.
    # AST's line numbers start indexing at 1.
    values: list[int] = []
    for x in ast.walk(node):
        if isinstance(x, ast.stmt | ast.ExceptHandler):
            # The lineno points to the class/def, so need to include the decorators.
            if isinstance(x, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                for d in x.decorator_list:
                    values.append(d.lineno - 1)
            values.append(x.lineno - 1)
            for name in ("finalbody", "orelse"):
                val: list[ast.stmt] | None = getattr(x, name, None)
                if val:
                    # Treat the finally/orelse part as its own statement.
                    values.append(val[0].lineno - 1 - 1)
    values.sort()
    insert_index = bisect_right(values, lineno)
    if insert_index == 0:
        return 0, None
    start = values[insert_index - 1]
    if insert_index >= len(values):
        end = None
    else:
        end = values[insert_index]
    return start, end

