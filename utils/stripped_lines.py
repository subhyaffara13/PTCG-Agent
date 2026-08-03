from typing import Callable

def stripped_lines(
    lines: Iterable[str],
    ignore_comments: bool,
    ignore_docstrings: bool,
    ignore_imports: bool,
    ignore_signatures: bool,
    line_enabled_callback: Callable[[str, int], bool] | None = None,
) -> list[LineSpecifs]:
    """Return tuples of line/line number/line type with leading/trailing white-space and
    any ignored code features removed.

    :param lines: a collection of lines
    :param ignore_comments: if true, any comment in the lines collection is removed from the result
    :param ignore_docstrings: if true, any line that is a docstring is removed from the result
    :param ignore_imports: if true, any line that is an import is removed from the result
    :param ignore_signatures: if true, any line that is part of a function signature is removed from the result
    :param line_enabled_callback: If called with "R0801" and a line number, a return value of False will disregard
           the line
    :return: the collection of line/line number/line type tuples
    """
    ignore_lines: set[int] = set()
    if ignore_imports or ignore_signatures:
        tree = astroid.parse("".join(lines))
        if ignore_imports:
            ignore_lines.update(
                chain.from_iterable(
                    range(node.lineno, (node.end_lineno or node.lineno) + 1)
                    for node in tree.nodes_of_class((nodes.Import, nodes.ImportFrom))
                )
            )
        if ignore_signatures:

            def _get_functions(
                functions: list[nodes.NodeNG], tree: nodes.NodeNG
            ) -> list[nodes.NodeNG]:
                """Recursively get all functions including nested in the classes from
                the.

                tree.
                """
                for node in tree.body:
                    if isinstance(node, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
                        functions.append(node)

                    if isinstance(
                        node,
                        (nodes.ClassDef, nodes.FunctionDef, nodes.AsyncFunctionDef),
                    ):
                        _get_functions(functions, node)

                return functions

            functions = _get_functions([], tree)
            ignore_lines.update(
                chain.from_iterable(
                    range(
                        func.lineno,
                        func.body[0].lineno if func.body else func.tolineno + 1,
                    )
                    for func in functions
                )
            )

    strippedlines = []
    docstring = None
    for lineno, line in enumerate(lines, start=1):
        if line_enabled_callback is not None and not line_enabled_callback(
            "R0801", lineno
        ):
            continue
        line = line.strip()
        if ignore_docstrings:
            if not docstring:
                if line.startswith(('"""', "'''")):
                    docstring = line[:3]
                    line = line[3:]
                elif line.startswith(('r"""', "r'''")):
                    docstring = line[1:4]
                    line = line[4:]
            if docstring:
                if line.endswith(docstring):
                    docstring = None
                line = ""
        if ignore_comments:
            line = line.split("#", 1)[0].strip()
        if lineno in ignore_lines:
            line = ""
        if line:
            strippedlines.append(
                LineSpecifs(text=line, line_number=LineNumber(lineno - 1))
            )
    return strippedlines

