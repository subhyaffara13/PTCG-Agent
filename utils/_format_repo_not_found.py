
def _format_repo_not_found(error: RepositoryNotFoundError) -> str:
    label = error.repo_type.capitalize() if error.repo_type else "Repository"
    if error.repo_id:
        msg = f"{label} '{error.repo_id}' not found."
    else:
        msg = f"{label} not found."
    msg += "\nIf the repo is private, make sure you are authenticated and your token has the required permissions."

    msg += "\nIf the repo does not exist, create it with: "
    if error.repo_id is not None:
        type_flag = f" --type {error.repo_type}" if error.repo_type and error.repo_type != "model" else ""
        msg += f"hf repos create {error.repo_id}{type_flag}"
    else:
        msg += "hf repos create <repo_id>"

    return msg

