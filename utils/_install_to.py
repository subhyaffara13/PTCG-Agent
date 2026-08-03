from pathlib import Path


def _install_to(skills_dir: Path, skill_name: str, force: bool) -> Path:
    """Install a marketplace skill into a skills directory. Returns the installed path."""
    try:
        return _skills.add_skill(skill_name, skills_dir, force=force)
    except FileExistsError as exc:
        raise CLIError(f"{exc}\nRe-run with --force to overwrite.") from exc

