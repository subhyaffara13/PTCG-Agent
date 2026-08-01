
def _format_local_entry_not_found(error: LocalEntryNotFoundError) -> str:
    cause = error.__cause__
    if cause is not None:
        return f"Local entry not found. {cause}"
    return f"Local entry not found. {error}"

