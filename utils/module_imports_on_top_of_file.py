
def module_imports_on_top_of_file(
        logical_line, indent_level, checker_state, noqa):
    r"""Place imports at the top of the file.

    Always put imports at the top of the file, just after any module
    comments and docstrings, and before module globals and constants.

    Okay: import os
    Okay: # this is a comment\nimport os
    Okay: '''this is a module docstring'''\nimport os
    Okay: r'''this is a module docstring'''\nimport os
    E402: a=1\nimport os
    E402: 'One string'\n"Two string"\nimport os
    E402: a=1\nfrom sys import x

    Okay: if x:\n    import os
    """  # noqa
    def is_string_literal(line):
        if line[0] in 'uUbB':
            line = line[1:]
        if line and line[0] in 'rR':
            line = line[1:]
        return line and (line[0] == '"' or line[0] == "'")

    allowed_keywords = (
        'try', 'except', 'else', 'finally', 'with', 'if', 'elif')

    if indent_level:  # Allow imports in conditional statement/function
        return
    if not logical_line:  # Allow empty lines or comments
        return
    if noqa:
        return
    line = logical_line
    if line.startswith('import ') or line.startswith('from '):
        if checker_state.get('seen_non_imports', False):
            yield 0, "E402 module level import not at top of file"
    elif re.match(DUNDER_REGEX, line):
        return
    elif any(line.startswith(kw) for kw in allowed_keywords):
        # Allow certain keywords intermixed with imports in order to
        # support conditional or filtered importing
        return
    elif is_string_literal(line):
        # The first literal is a docstring, allow it. Otherwise, report
        # error.
        if checker_state.get('seen_docstring', False):
            checker_state['seen_non_imports'] = True
        else:
            checker_state['seen_docstring'] = True
    else:
        checker_state['seen_non_imports'] = True

