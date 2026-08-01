
def fix_cobertura_filename(line: str) -> str:
    r"""Changes filename paths to Linux paths in Cobertura output files.

    E.g. filename="pkg\subpkg\a.py" -> filename="pkg/subpkg/a.py".
    """
    m = re.search(r'<class .* filename="(?P<filename>.*?)"', line)
    if not m:
        return line
    return "{}{}{}".format(
        line[: m.start(1)], m.group("filename").replace("\\", "/"), line[m.end(1) :]
    )

