
def _format_entry_not_found(error: RemoteEntryNotFoundError) -> str:
    label = error.repo_type if error.repo_type else "repository"
    url = str(error.response.url) if error.response else None
    if error.repo_id:
        msg = f"File not found in {label} '{error.repo_id}'."
    else:
        msg = f"File not found in {label}."
    if url:
        msg += f"\nURL: {url}"
    return msg

