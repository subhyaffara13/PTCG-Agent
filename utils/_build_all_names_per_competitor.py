
def _build_all_names_per_competitor(
    competitors: list[str], variations_map: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Build canonical + variation name lists for each competitor."""
    return {comp: [comp] + variations_map.get(comp, []) for comp in competitors}

