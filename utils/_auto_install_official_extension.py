from pathlib import Path


def _auto_install_official_extension(short_name: str) -> Path | None:
    """Try to auto-install huggingface/hf-<name>. Returns executable path or None."""
    owner, repo_name = DEFAULT_EXTENSION_OWNER, f"hf-{short_name}"
    try:
        extension_dir = _get_extension_dir(short_name)
    except Exception:
        return None
    if extension_dir.exists():
        return None
    try:
        response = get_session().get(
            f"https://api.github.com/repos/{owner}/{repo_name}",
            follow_redirects=True,
            timeout=_EXTENSIONS_DOWNLOAD_TIMEOUT,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        branch = response.json()["default_branch"]
    except Exception:
        return None
    try:
        out.confirm(f"'{short_name}' is an official Hugging Face extension ({owner}/{repo_name}). Install it?")
    except ConfirmationError:
        return None
    try:
        manifest = _install_extension_from_github(
            owner=owner, repo_name=repo_name, short_name=short_name, extension_dir=extension_dir, branch=branch
        )
        return Path(manifest.executable_path).expanduser()
    except Exception:
        shutil.rmtree(extension_dir, ignore_errors=True)
        return None

