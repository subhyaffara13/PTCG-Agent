import os
from pathlib import Path


def _install_binary_extension(
    *, owner: str, repo_name: str, short_name: str, extension_dir: Path, binary: bytes
) -> ExtensionManifest:
    # Save extension binary
    executable_name = _get_executable_name(short_name)
    extension_dir.mkdir(parents=True, exist_ok=False)
    executable_path = extension_dir / executable_name
    executable_path.write_bytes(binary)

    # Make it executable
    if os.name != "nt":
        os.chmod(executable_path, 0o755)

    # Create manifest
    return ExtensionManifest(
        owner=owner,
        repo=repo_name,
        repo_id=f"{owner}/{repo_name}",
        short_name=short_name,
        executable_name=executable_name,
        executable_path=str(executable_path),
        type="binary",
        installed_at=datetime.now(timezone.utc),
        source=f"https://github.com/{owner}/{repo_name}",
    )

