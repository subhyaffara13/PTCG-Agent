
def print_usage_error(e: UsageError, file: TextIO) -> None:
    tw = TerminalWriter(file)
    for msg in e.args:
        tw.line(f"ERROR: {msg}\n", red=True)

