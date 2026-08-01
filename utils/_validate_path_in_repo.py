
def _validate_path_in_repo(path_in_repo: str) -> str:
    # Validate `path_in_repo` value to prevent a server-side issue
    if path_in_repo.startswith("/"):
        path_in_repo = path_in_repo[1:]
    if path_in_repo == "." or path_in_repo == ".." or path_in_repo.startswith("../"):
        raise ValueError(f"Invalid `path_in_repo` in CommitOperation: '{path_in_repo}'")
    if path_in_repo.startswith("./"):
        path_in_repo = path_in_repo[2:]
    for forbidden in FORBIDDEN_FOLDERS:
        if any(part == forbidden for part in path_in_repo.split("/")):
            raise ValueError(
                f"Invalid `path_in_repo` in CommitOperation: cannot update files under a '{forbidden}/' folder (path:"
                f" '{path_in_repo}')."
            )
    return path_in_repo

