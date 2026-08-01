
def build_cells(
    variants: Iterable[str],
    models: list[str],
    games_per_matchup: int,
    *,
    include_self_play: bool,
) -> list[GameCell]:
    """Enumerate every cell to play (K * M(M-1)/2 * games + optional self-play).

    For each variant, each unordered model pair contributes
    ``games_per_matchup`` games -- ``games_per_matchup / 2`` seat-flipped
    pairs sharing one chance seed each.
    """
    if games_per_matchup % 2 != 0:
        raise SystemExit(
            f"--games must be even (got {games_per_matchup}); each "
            f"matchup is scheduled in seat-flipped pairs."
        )
    pairs_per_matchup = games_per_matchup // 2
    cells: list[GameCell] = []
    for v in variants:
        # Round-robin over unordered model pairs.
        for i, a in enumerate(models):
            for b in models[i + 1 :]:
                for pair_idx in range(pairs_per_matchup):
                    cells.append(GameCell(v, a, b, seed=pair_idx, pair_role="AB"))
                    cells.append(GameCell(v, b, a, seed=pair_idx, pair_role="BA"))
            if include_self_play:
                for game_idx in range(games_per_matchup):
                    cells.append(
                        GameCell(v, a, a, seed=game_idx, pair_role="SELF")
                    )
    return cells

