
def _load_archetype_data(arch_file):
    import json, logging
    logger = logging.getLogger("MetaTeam")
    if arch_file.exists():
        try:
            return json.loads(arch_file.read_text(encoding="utf-8")).get("archetypes", {})
        except Exception as e: logger.error(f"Failed to load deck archetypes for analysis: {e}")
    return {}

