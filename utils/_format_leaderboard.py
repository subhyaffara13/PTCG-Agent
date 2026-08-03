from typing import Any
import math


def _format_leaderboard(
    variant: str,
    models: list[str],
    agg: dict[str, Any],
) -> str:
    """Render one leaderboard section for summary.md."""
    rows: list[tuple[str, float, float, float, float, float]] = []
    for m in models:
        gp = agg["games_played"].get((variant, m), 0)
        if gp == 0:
            continue
        pair_n = agg["pair_counts"].get((variant, m), 0)
        pair_win_pct = (
            100.0 * agg["pair_wins"].get((variant, m), 0.0) / pair_n
            if pair_n else float("nan")
        )
        game_win_pct = 100.0 * agg["game_wins"].get((variant, m), 0.0) / gp
        mean_score = agg["score_sum"].get((variant, m), 0.0) / max(gp, 1)
        crash_pct = 100.0 * agg["crash_count"].get((variant, m), 0) / gp
        rows.append((m, pair_win_pct, game_win_pct, mean_score, crash_pct, gp))
    rows.sort(
        # Sort by pair-win% desc, fall back to game-win% if all-self-play.
        key=lambda r: (-r[1] if not math.isnan(r[1]) else -r[2], -r[2]),
    )
    lines = [
        f"## Leaderboard: {variant}",
        "",
        "| model | pair-win% | game-win% | mean score | crash% | games |",
        "|-------|-----------|-----------|------------|--------|-------|",
    ]
    for m, pwin, gwin, sc, cr, gp in rows:
        pwin_str = "—" if math.isnan(pwin) else f"{pwin:.1f}"
        lines.append(
            f"| {m} | {pwin_str} | {gwin:.1f} | {sc:+.2f} | {cr:.1f} | {gp} |"
        )
    return "\n".join(lines)

