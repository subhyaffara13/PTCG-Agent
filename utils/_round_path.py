
def _round_path(
    path: pathops.Path, round: Callable[[float], float] = otRound
) -> pathops.Path:
    rounded_path = pathops.Path()
    for verb, points in path:
        rounded_path.add(verb, *((round(p[0]), round(p[1])) for p in points))
    return rounded_path

