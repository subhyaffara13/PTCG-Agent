from typing import Any

def _extract_source_from_frame(cls: type[Any]) -> list[str] | None:
    frame = inspect.currentframe()

    while frame:
        if inspect.getmodule(frame) is inspect.getmodule(cls):
            lnum = frame.f_lineno
            try:
                lines, _ = inspect.findsource(frame)
            except OSError:  # pragma: no cover
                # Source can't be retrieved (maybe because running in an interactive terminal),
                # we don't want to error here.
                pass
            else:
                block_lines = inspect.getblock(lines[lnum - 1 :])
                dedent_source = _dedent_source_lines(block_lines)
                try:
                    block_tree = ast.parse(dedent_source)
                except SyntaxError:
                    pass
                else:
                    stmt = block_tree.body[0]
                    if isinstance(stmt, ast.FunctionDef) and stmt.name == 'dedent_workaround':
                        # `_dedent_source_lines` wrapped the class around the workaround function
                        stmt = stmt.body[0]
                    if isinstance(stmt, ast.ClassDef) and stmt.name == cls.__name__:
                        return block_lines

        frame = frame.f_back

