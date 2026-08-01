
def count_stats(messages: list[str]) -> tuple[int, int, int]:
    """Count total number of errors, notes and error_files in message list."""
    errors = [e for e in messages if ": error:" in e]
    error_files = {e.split(":")[0] for e in errors}
    notes = [e for e in messages if ": note:" in e]
    return len(errors), len(notes), len(error_files)

