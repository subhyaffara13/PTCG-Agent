
def _apply_single_update(api, skill_dir: Path, marketplace_skills: dict[str, MarketplaceSkill]) -> SkillUpdateInfo:
    base = SkillUpdateInfo(name=skill_dir.name, skill_dir=skill_dir, status="unmanaged")

    if not (skill_dir / MANAGED_MARKER_FILENAME).exists():
        return base

    skill = marketplace_skills.get(skill_dir.name.lower())
    if skill is None:
        return replace(
            base,
            status="source_unreachable",
            detail=f"Skill '{skill_dir.name}' is no longer available in {DEFAULT_SKILLS_BUCKET_ID}.",
        )

    try:
        _install_marketplace_skill(api, skill, skill_dir.parent, force=True)
    except Exception as exc:
        return replace(base, status="source_unreachable", detail=str(exc))

    return replace(base, status="up_to_date")

