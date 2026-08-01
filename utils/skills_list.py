
def skills_list(
    token: TokenOpt = None,
) -> None:
    """List available skills from the Hugging Face marketplace."""
    install_locations: list[tuple[str, Path]] = [
        ("project", CENTRAL_LOCAL),
        ("project (claude)", CLAUDE_LOCAL),
        ("global", CENTRAL_GLOBAL),
        ("global (claude)", CLAUDE_GLOBAL),
    ]
    installed: dict[str, set[str]] = {}
    for label, root in install_locations:
        for skill_dir in _skills._iter_unique_skill_dirs([root]):
            installed.setdefault(skill_dir.name.lower(), set()).add(label)

    api = get_hf_api(token=token)
    with disable_progress_bars():
        skills = _skills._load_marketplace_skills(api)
    results = [
        {
            "name": skill.name,
            "description": skill.description or "",
            **{
                label: "yes" if label in installed.get(skill.name.lower(), set()) else ""
                for label, _ in install_locations
            },
        }
        for skill in skills
    ]
    out.table(
        results,
        id_key="name",
        alignments={"project": "right", "global": "right", "project (claude)": "right", "global (claude)": "right"},
    )

