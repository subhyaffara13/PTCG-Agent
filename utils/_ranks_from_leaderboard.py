
def _ranks_from_leaderboard(
    leaderboard: list[tuple[str, float]],
) -> dict[str, int]:
    return {m: i + 1 for i, (m, _) in enumerate(leaderboard)}

