
def _format_revision_not_found(error: RevisionNotFoundError) -> str:
    label = error.repo_type if error.repo_type else "repository"
    if error.repo_id:
        return f"Revision not found in {label} '{error.repo_id}'."
    return f"Revision not found in {label}. Check the revision parameter."

