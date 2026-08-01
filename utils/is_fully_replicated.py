
def is_fully_replicated(placements: tuple[Placement, ...]) -> bool:
    """Check if all placements are Replicate."""
    return all(isinstance(p, Replicate) for p in placements)

