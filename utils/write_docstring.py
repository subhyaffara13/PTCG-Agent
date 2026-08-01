
def write_docstring(tw: TerminalWriter, doc: str, indent: str = "    ") -> None:
    for line in doc.split("\n"):
        tw.line(indent + line)

