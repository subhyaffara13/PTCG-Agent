
def render_summary(
    env_name: str,
    variants: list[str],
    models: list[str],
    rows: list[dict[str, Any]],
) -> str:
    """Render the full summary.md content for ``rows``."""
    agg = _aggregate(rows)
    parts = [
        f"# Ablation results: {env_name}",
        "",
        f"Variants: {', '.join(variants)}",
        f"Models: {', '.join(models)}",
        f"Total games: {len(rows)}",
        "",
    ]
    for v in variants:
        parts.append(_format_leaderboard(v, models, agg))
        parts.append("")
    rank_shifts = _format_rank_shifts(variants, models, agg)
    if rank_shifts:
        parts.append(rank_shifts)
        parts.append("")
    parts.append(_format_anomalies(rows))
    parts.append("")
    return "\n".join(parts)

