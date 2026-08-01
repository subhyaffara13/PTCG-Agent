
def deindent(lines: Iterable[str]) -> list[str]:
    return textwrap.dedent("\n".join(lines)).splitlines()

