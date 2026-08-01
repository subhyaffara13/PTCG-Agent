
def blank_lines(logical_line, blank_lines, indent_level, line_number,
                blank_before, previous_logical,
                previous_unindented_logical_line, previous_indent_level,
                lines):
    r"""Separate top-level function and class definitions with two blank
    lines.

    Method definitions inside a class are separated by a single blank
    line.

    Extra blank lines may be used (sparingly) to separate groups of
    related functions.  Blank lines may be omitted between a bunch of
    related one-liners (e.g. a set of dummy implementations).

    Use blank lines in functions, sparingly, to indicate logical
    sections.

    Okay: def a():\n    pass\n\n\ndef b():\n    pass
    Okay: def a():\n    pass\n\n\nasync def b():\n    pass
    Okay: def a():\n    pass\n\n\n# Foo\n# Bar\n\ndef b():\n    pass
    Okay: default = 1\nfoo = 1
    Okay: classify = 1\nfoo = 1

    E301: class Foo:\n    b = 0\n    def bar():\n        pass
    E302: def a():\n    pass\n\ndef b(n):\n    pass
    E302: def a():\n    pass\n\nasync def b(n):\n    pass
    E303: def a():\n    pass\n\n\n\ndef b(n):\n    pass
    E303: def a():\n\n\n\n    pass
    E304: @decorator\n\ndef a():\n    pass
    E305: def a():\n    pass\na()
    E306: def a():\n    def b():\n        pass\n    def c():\n        pass
    """  # noqa
    top_level_lines = BLANK_LINES_CONFIG['top_level']
    method_lines = BLANK_LINES_CONFIG['method']

    if not previous_logical and blank_before < top_level_lines:
        return  # Don't expect blank lines before the first line
    if previous_logical.startswith('@'):
        if blank_lines:
            yield 0, "E304 blank lines found after function decorator"
    elif (blank_lines > top_level_lines or
            (indent_level and blank_lines == method_lines + 1)
          ):
        yield 0, "E303 too many blank lines (%d)" % blank_lines
    elif STARTSWITH_TOP_LEVEL_REGEX.match(logical_line):
        # allow a group of one-liners
        if (
            _is_one_liner(logical_line, indent_level, lines, line_number) and
            blank_before == 0
        ):
            return
        if indent_level:
            if not (blank_before == method_lines or
                    previous_indent_level < indent_level or
                    DOCSTRING_REGEX.match(previous_logical)
                    ):
                ancestor_level = indent_level
                nested = False
                # Search backwards for a def ancestor or tree root
                # (top level).
                for line in lines[line_number - top_level_lines::-1]:
                    if line.strip() and expand_indent(line) < ancestor_level:
                        ancestor_level = expand_indent(line)
                        nested = STARTSWITH_DEF_REGEX.match(line.lstrip())
                        if nested or ancestor_level == 0:
                            break
                if nested:
                    yield 0, "E306 expected %s blank line before a " \
                        "nested definition, found 0" % (method_lines,)
                else:
                    yield 0, "E301 expected {} blank line, found 0".format(
                        method_lines)
        elif blank_before != top_level_lines:
            yield 0, "E302 expected %s blank lines, found %d" % (
                top_level_lines, blank_before)
    elif (logical_line and
            not indent_level and
            blank_before != top_level_lines and
            previous_unindented_logical_line.startswith(('def ', 'class '))
          ):
        yield 0, "E305 expected %s blank lines after " \
            "class or function definition, found %d" % (
                top_level_lines, blank_before)

