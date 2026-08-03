from pathlib import Path


def update_skills(roots: list[Path], selector: str | None = None) -> list[SkillUpdateInfo]:
    """Re-sync managed marketplace skill installs from the bucket."""
    skill_dirs = _iter_unique_skill_dirs(roots)
    if selector is not None:
        selector_lower = selector.strip().lower()
        skill_dirs = [d for d in skill_dirs if d.name.lower() == selector_lower]
        if not skill_dirs:
            raise CLIError(f"No installed skill matches '{selector}'. Install it with `hf skills add {selector}`.")

    api = get_hf_api()
    with disable_progress_bars():
        marketplace_skills = {skill.name.lower(): skill for skill in _load_marketplace_skills(api)}
        return [_apply_single_update(api, skill_dir, marketplace_skills) for skill_dir in skill_dirs]

