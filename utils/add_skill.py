from pathlib import Path


def add_skill(skill_name: str, destination_root: Path, force: bool = False) -> Path:
    """Resolve a marketplace skill by name and install it."""
    api = get_hf_api()
    with disable_progress_bars():
        marketplace_skills = _load_marketplace_skills(api)
        skill = _select_marketplace_skill(marketplace_skills, skill_name)
        if skill is None:
            raise CLIError(
                f"Skill '{skill_name}' not found in {DEFAULT_SKILLS_BUCKET_ID}. "
                "Try `hf skills add` to install `hf-cli` or use a known skill name."
            )
        return _install_marketplace_skill(api, skill, destination_root, force=force)

