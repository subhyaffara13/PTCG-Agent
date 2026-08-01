
def _build_comparison_blocked_words(
    competitors: list[str], all_names: dict[str, list[str]], brand_name: str
) -> list[dict]:
    """Build blocked word entries for unfavorable competitor comparisons."""
    result = []
    for comp in competitors:
        for name in all_names[comp]:
            result.append(
                {
                    "keyword": f"{name} is better",
                    "action": "BLOCK",
                    "description": f"Unfavorable comparison ({comp})",
                }
            )

    # Brand-level comparisons (only need one entry each, not per-competitor)
    result.append(
        {
            "keyword": f"better than {brand_name}",
            "action": "BLOCK",
            "description": "Unfavorable comparison",
        }
    )
    result.append(
        {
            "keyword": f"{brand_name} is worse",
            "action": "BLOCK",
            "description": "Unfavorable comparison",
        }
    )

    return result

