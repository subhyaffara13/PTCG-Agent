from pathlib import Path


def _install_extension_from_github(
    *,
    owner: str,
    repo_name: str,
    short_name: str,
    extension_dir: Path,
    branch: str,
    description: str | None = None,
) -> ExtensionManifest:
    """Fetch, install (binary or Python), and save manifest for a GitHub extension."""
    try:
        binary = _fetch_remote_binary(owner=owner, repo_name=repo_name, branch=branch, short_name=short_name)
    except Exception:
        binary = None
    if binary is not None:
        manifest = _install_binary_extension(
            owner=owner, repo_name=repo_name, short_name=short_name, extension_dir=extension_dir, binary=binary
        )
    else:
        manifest = _install_python_extension(
            owner=owner, repo_name=repo_name, short_name=short_name, extension_dir=extension_dir, branch=branch
        )
    manifest.description = _try_fetch_remote_description(
        owner=owner, repo_name=repo_name, branch=branch, candidate_description=description
    )
    manifest.save(extension_dir)
    return manifest

