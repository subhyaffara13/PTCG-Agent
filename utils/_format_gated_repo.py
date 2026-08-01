
def _format_gated_repo(error: GatedRepoError) -> str:
    label = error.repo_type if error.repo_type else "repository"
    if error.repo_id:
        return f"Access denied. {label.capitalize()} '{error.repo_id}' requires approval."
    return f"Access denied. This {label} requires approval."

