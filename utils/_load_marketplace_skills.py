
def _load_marketplace_skills(api) -> list[MarketplaceSkill]:
    payload = _load_marketplace_payload(api)
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        raise CLIError("Invalid marketplace payload: expected a top-level 'plugins' list.")

    skills: list[MarketplaceSkill] = []
    for plugin in plugins:
        if not isinstance(plugin, dict):
            continue
        name = plugin.get("name")
        source = plugin.get("source")
        if not isinstance(name, str) or not isinstance(source, str):
            continue
        description = plugin.get("description")
        skills.append(
            MarketplaceSkill(
                name=name,
                repo_path=_normalize_repo_path(source),
                description=description if isinstance(description, str) else None,
            )
        )
    return skills

