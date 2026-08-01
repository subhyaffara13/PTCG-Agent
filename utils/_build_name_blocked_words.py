
def _build_name_blocked_words(
    competitors: list[str], all_names: dict[str, list[str]]
) -> list[dict]:
    """Build blocked word entries for direct competitor name mentions."""
    result = []
    for comp in competitors:
        for name in all_names[comp]:
            desc = (
                f"Competitor: {comp}"
                if name == comp
                else f"Competitor variation ({comp}): {name}"
            )
            result.append({"keyword": name, "action": "BLOCK", "description": desc})
    return result

