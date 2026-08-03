import os

def _resolve_upload_paths(
    *, repo_id: str, local_path: str | None, path_in_repo: str | None, include: list[str] | None
) -> tuple[str, str, list[str] | None]:
    repo_name = repo_id.split("/")[-1]
    resolved_include = include

    if local_path is not None and any(c in local_path for c in ["*", "?", "["]):
        if include is not None:
            raise ValueError("Cannot set --include when local_path contains a wildcard.")
        if path_in_repo is not None and path_in_repo != ".":
            raise ValueError("Cannot set path_in_repo when local_path contains a wildcard.")
        return ".", local_path, ["."]  # will be adjusted below; placeholder for type

    if local_path is None and os.path.isfile(repo_name):
        return repo_name, repo_name, resolved_include
    if local_path is None and os.path.isdir(repo_name):
        return repo_name, ".", resolved_include
    if local_path is None:
        raise ValueError(f"'{repo_name}' is not a local file or folder. Please set local_path explicitly.")

    if path_in_repo is None and os.path.isfile(local_path):
        return local_path, os.path.basename(local_path), resolved_include
    if path_in_repo is None:
        return local_path, ".", resolved_include
    return local_path, path_in_repo, resolved_include

