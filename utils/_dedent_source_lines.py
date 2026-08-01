
def _dedent_source_lines(source: list[str]) -> str:
    # Required for nested class definitions, e.g. in a function block
    dedent_source = textwrap.dedent(''.join(source))
    if dedent_source.startswith((' ', '\t')):
        # We are in the case where there's a dedented (usually multiline) string
        # at a lower indentation level than the class itself. We wrap our class
        # in a function as a workaround.
        dedent_source = f'def dedent_workaround():\n{dedent_source}'
    return dedent_source

