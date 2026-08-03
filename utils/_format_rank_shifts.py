from typing import Any

def _format_rank_shifts(
    variants: list[str],
    models: list[str],
    agg: dict[str, Any],
) -> str:
    """Cross-variant rank-of-each-model table -- the artifact worth reading."""
    # Within each variant, rank models by pair-win% (game-win% fallback).
    ranks: dict[tuple[str, str], int] = {}
    for v in variants:
        scored: list[tuple[str, float]] = []
        for m in models:
            gp = agg["games_played"].get((v, m), 0)
            if gp == 0:
                continue
            pair_n = agg["pair_counts"].get((v, m), 0)
            primary = (
                agg["pair_wins"].get((v, m), 0.0) / pair_n if pair_n
                else agg["game_wins"].get((v, m), 0.0) / gp
            )
            scored.append((m, primary))
        scored.sort(key=lambda x: -x[1])
        for rank, (m, _) in enumerate(scored, start=1):
            ranks[(v, m)] = rank

    if not ranks:
        return ""

    width = max(len(m) for m in models)
    header = "| " + "model".ljust(width) + " | " + " | ".join(v for v in variants) + " |"
    sep = "|" + "-" * (width + 2) + "|" + "|".join("-" * (len(v) + 2) for v in variants) + "|"
    lines = ["## Cross-variant rank shifts", "", header, sep]
    for m in models:
        cells = [str(ranks.get((v, m), "—")).center(len(v)) for v in variants]
        lines.append("| " + m.ljust(width) + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)

