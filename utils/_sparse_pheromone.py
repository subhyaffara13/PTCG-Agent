
def _sparse_pheromone(
    pheromone: list[list[float]] | None,
    threshold: float = _PHEROMONE_THRESHOLD,
) -> str:
    if not pheromone:
        return "(none)"
    items: list[str] = []
    for r, row in enumerate(pheromone):
        for c, v in enumerate(row):
            if float(v) >= threshold:
                items.append(f"[{r},{c}]={float(v):.2f}")
    return ", ".join(items) if items else "(none)"


def _sparse_pheromone(
    pheromone: list[list[float]] | None,
    threshold: float = _PHEROMONE_THRESHOLD,
) -> str:
    """List cells whose pheromone value is at least ``threshold``."""
    if not pheromone:
        return "(none)"
    items: list[str] = []
    for r, row in enumerate(pheromone):
        for c, v in enumerate(row):
            if float(v) >= threshold:
                items.append(f"[{r},{c}]={float(v):.2f}")
    return ", ".join(items) if items else "(none)"

