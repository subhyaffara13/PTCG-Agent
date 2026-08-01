
def mi_parameters(code, count_multi=True):
    '''Given a source code snippet, compute the necessary parameters to
    compute the Maintainability Index metric. These include:

        * the Halstead Volume
        * the Cyclomatic Complexity
        * the number of LLOC (Logical Lines of Code)
        * the percent of lines of comment

    :param multi: If True, then count multiline strings as comment lines as
        well. This is not always safe because Python multiline strings are not
        always docstrings.
    '''
    ast_node = ast.parse(code)
    raw = analyze(code)
    comments_lines = raw.comments + (raw.multi if count_multi else 0)
    comments = comments_lines / float(raw.sloc) * 100 if raw.sloc != 0 else 0
    return (
        h_visit_ast(ast_node).total.volume,
        ComplexityVisitor.from_ast(ast_node).total_complexity,
        raw.lloc,
        comments,
    )

