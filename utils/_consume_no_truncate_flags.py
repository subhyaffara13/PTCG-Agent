
def _consume_no_truncate_flags(args: list[str]) -> bool:
    """Strip all global --no-truncate flags from args and return whether any was provided."""
    no_truncate = False
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--":
            break  # everything after '--' is a positional literal
        if arg == "--no-truncate":
            no_truncate = True
            del args[i : i + 1]
            continue
        if arg.startswith("--no-truncate="):
            raise click.UsageError("Option '--no-truncate' does not take a value.")
        i += 1
    return no_truncate

