
def _build_recommendation_blocked_words(
    competitors: list[str], all_names: dict[str, list[str]]
) -> list[dict]:
    """Build blocked word entries for competitor recommendations."""
    result = []
    for comp in competitors:
        for name in all_names[comp]:
            for prefix in ["try", "use", "switch to", "consider"]:
                result.append(
                    {
                        "keyword": f"{prefix} {name}",
                        "action": "BLOCK",
                        "description": f"Recommendation to competitor ({comp})",
                    }
                )
    return result

